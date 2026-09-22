import os
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

class DownloadPaused(Exception): pass
class DownloadCancelled(Exception): pass

class DownloadManager:
    def __init__(self, max_workers=2):
        self.jobs = {}
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def add_batch(self, urls, format_id, mode="video", audio_format="mp3"):
        return [self.add(url, format_id, mode, audio_format) for url in urls]

    def add(self, url, format_id, mode="video", audio_format="mp3"):
        job_id = uuid.uuid4().hex[:10]
        job = {
            "id": job_id, "url": url, "format_id": format_id,
            "mode": mode, "audio_format": audio_format,
            "status": "queued", "progress": 0, "speed": None,
            "eta": None, "title": "Preparing...", "error": None,
            "pause": False, "cancel": False, "retries": 0
        }
        with self.lock:
            self.jobs[job_id] = job
        self.executor.submit(self._run, job_id)
        return job

    def _run(self, job_id):
        while True:
            with self.lock:
                job = self.jobs[job_id]
                if job["cancel"]:
                    job["status"] = "cancelled"
                    return
                job["pause"] = False
                job["status"] = "downloading"

            try:
                self._download(job_id)
                with self.lock:
                    job = self.jobs[job_id]
                    if job["cancel"]:
                        job["status"] = "cancelled"
                    else:
                        job["status"] = "completed"
                        job["progress"] = 100
                return
            except DownloadPaused:
                with self.lock:
                    if self.jobs[job_id]["cancel"]:
                        self.jobs[job_id]["status"] = "cancelled"
                        return
                    self.jobs[job_id]["status"] = "paused"
                while True:
                    with self.lock:
                        job = self.jobs[job_id]
                        if job["cancel"]:
                            job["status"] = "cancelled"
                            return
                        if not job["pause"]:
                            break
                    threading.Event().wait(0.25)
            except DownloadCancelled:
                with self.lock:
                    self.jobs[job_id]["status"] = "cancelled"
                return
            except Exception as e:
                with self.lock:
                    job = self.jobs[job_id]
                    job["retries"] += 1
                    if job["retries"] <= 2 and not job["cancel"]:
                        job["status"] = "retrying"
                        continue
                    job["status"] = "failed"
                    job["error"] = str(e)
                return

    def _download(self, job_id):
        with self.lock:
            job = self.jobs[job_id]

        def hook(data):
            with self.lock:
                j = self.jobs[job_id]
                if j["cancel"]:
                    raise DownloadCancelled()
                if j["pause"]:
                    raise DownloadPaused()
                j["title"] = data.get("filename", j["title"]).split(os.sep)[-1]
                if data.get("status") == "downloading":
                    j["progress"] = round(data.get("_percent", 0), 1)
                    j["speed"] = data.get("_speed_str")
                    j["eta"] = data.get("_eta_str")

        if job["mode"] == "audio":
            opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                "noplaylist": True, "continuedl": True,
                "progress_hooks": [hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": job["audio_format"],
                    "preferredquality": "192"
                }]
            }
        else:
            opts = {
                "format": f'{job["format_id"]}+bestaudio/best',
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                "noplaylist": True, "continuedl": True,
                "merge_output_format": "mp4",
                "progress_hooks": [hook]
            }

        with YoutubeDL(opts) as ydl:
            ydl.download([job["url"]])

    def pause(self, job_id):
        with self.lock:
            if job_id in self.jobs and self.jobs[job_id]["status"] == "downloading":
                self.jobs[job_id]["pause"] = True
                return True
        return False

    def resume(self, job_id):
        with self.lock:
            if job_id in self.jobs and self.jobs[job_id]["status"] == "paused":
                self.jobs[job_id]["pause"] = False
                return True
        return False

    def cancel(self, job_id):
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]["cancel"] = True
                return True
        return False

    def retry(self, job_id):
        with self.lock:
            if job_id not in self.jobs or self.jobs[job_id]["status"] != "failed":
                return False
            self.jobs[job_id]["retries"] = 0
            self.jobs[job_id]["error"] = None
            self.jobs[job_id]["status"] = "queued"
            self.jobs[job_id]["cancel"] = False
        self.executor.submit(self._run, job_id)
        return True

    def all(self):
        with self.lock:
            return list(self.jobs.values())

manager = DownloadManager()

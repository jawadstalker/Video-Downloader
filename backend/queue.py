import os
import shutil
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


class DownloadPaused(Exception):
    pass


class DownloadCancelled(Exception):
    pass


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
            job = self.jobs[job_id].copy()

        def hook(data):
            with self.lock:
                current = self.jobs[job_id]
                if current["cancel"]:
                    raise DownloadCancelled()
                if current["pause"]:
                    raise DownloadPaused()

                filename = data.get("filename")
                if filename:
                    current["title"] = os.path.basename(filename)

                if data.get("status") == "downloading":
                    total = data.get("total_bytes") or data.get("total_bytes_estimate")
                    downloaded = data.get("downloaded_bytes")
                    if total and downloaded is not None:
                        current["progress"] = round(downloaded / total * 100, 1)
                    current["speed"] = data.get("_speed_str")
                    current["eta"] = data.get("_eta_str")
                elif data.get("status") == "finished":
                    current["progress"] = 100

        opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "continuedl": True,
            "progress_hooks": [hook],
        }

        if job["mode"] == "audio":
            if shutil.which("ffmpeg") is None:
                raise RuntimeError("FFmpeg is required for audio extraction.")
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": job["audio_format"],
                "preferredquality": "192",
            }]
        else:
            format_id = job["format_id"]
            opts["format"] = format_id if "+" in format_id else f"{format_id}+bestaudio/best"
            if shutil.which("ffmpeg") is not None:
                opts["merge_output_format"] = "mp4"

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
            if job_id in self.jobs and self.jobs[job_id]["status"] in {
                "queued", "downloading", "paused", "retrying"
            }:
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
            self.jobs[job_id]["pause"] = False
            self.jobs[job_id]["progress"] = 0
        self.executor.submit(self._run, job_id)
        return True

    def all(self):
        with self.lock:
            return [job.copy() for job in self.jobs.values()]


manager = DownloadManager()

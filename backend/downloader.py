import os
import shutil
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def ffmpeg_available():
    return shutil.which("ffmpeg") is not None

def download(url, format_id, mode="video", audio_format="mp3"):
    if not url or not format_id:
        raise ValueError("URL and format are required.")

    if mode == "audio":
        if not ffmpeg_available():
            raise RuntimeError("FFmpeg is required for audio extraction.")

        opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "192",
            }],
        }
    else:
        opts = {
            "format": f"{format_id}+bestaudio[ext=m4a]/best",
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "merge_output_format": "mp4",
        }

        if not ffmpeg_available():
            opts["format"] = f"{format_id}/best[ext=mp4]/best"

    with YoutubeDL(opts) as ydl:
        ydl.download([url])

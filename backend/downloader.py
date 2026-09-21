import os
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download(url, format_id):
    if not url or not format_id:
        raise ValueError("URL and format are required.")

    opts = {
        "format": format_id,
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "merge_output_format": "mp4",
    }

    with YoutubeDL(opts) as ydl:
        ydl.download([url])

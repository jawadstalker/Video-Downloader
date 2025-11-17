from yt_dlp import YoutubeDL
import os

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_formats(url):
    """بازگرداندن فرمت‌های قابل دانلود ویدیوی یوتیوب"""
    ydl_opts_info = {"listformats": True}
    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])
        return [f for f in formats if f.get("height")]

def download_video(url, format_id):
    """دانلود ویدیو با فرمت انتخاب شده"""
    ydl_opts_download = {
        "format": format_id,
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "video_%(height)sp.%(ext)s"),
        "noplaylist": True,
    }
    with YoutubeDL(ydl_opts_download) as ydl:
        ydl.download([url])
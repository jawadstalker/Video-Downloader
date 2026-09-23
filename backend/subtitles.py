import os
import shutil
from yt_dlp import YoutubeDL

DOWNLOAD_FOLDER = "downloads"

ALLOWED_FORMATS = {"srt", "vtt", "ass", "lrc"}

def languages(info):
    return sorted((info.get("subtitles") or {}).keys())

def automatic_languages(info):
    return sorted((info.get("automatic_captions") or {}).keys())

def options(info):
    return sorted(set(languages(info)) | set(automatic_languages(info)))

def subtitle_formats(info, language):
    result = []
    for source_name, source in (
        ("subtitle", info.get("subtitles") or {}),
        ("automatic", info.get("automatic_captions") or {}),
    ):
        for item in source.get(language, []) or []:
            ext = item.get("ext")
            if ext and ext in ALLOWED_FORMATS:
                result.append({"source": source_name, "ext": ext})
    return sorted(result, key=lambda x: (x["source"], x["ext"]))

def download(url, languages_selected, output_format="srt", automatic=False):
    if not url:
        raise ValueError("URL is required.")
    if output_format not in ALLOWED_FORMATS:
        raise ValueError("Unsupported subtitle format.")
    if not languages_selected:
        raise ValueError("Select at least one subtitle language.")

    if shutil.which("ffmpeg") is None and output_format == "lrc":
        raise RuntimeError("FFmpeg is required for this subtitle format.")

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    opts = {
        "skip_download": True,
        "writesubtitles": not automatic,
        "writeautomaticsub": automatic,
        "subtitleslangs": languages_selected,
        "subtitlesformat": output_format,
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
        "noplaylist": True,
    }

    with YoutubeDL(opts) as ydl:
        ydl.download([url])

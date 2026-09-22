from yt_dlp import YoutubeDL

def _size(value):
    if not value:
        return None
    units = ["B", "KB", "MB", "GB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024

def _duration(seconds):
    if not seconds:
        return None
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def analyze_playlist(url):
    if not url or not url.strip():
        raise ValueError("Please enter a valid playlist URL.")
    opts = {"quiet": True, "no_warnings": True, "extract_flat": True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url.strip(), download=False)
    entries = []
    for item in info.get("entries") or []:
        if item and item.get("url"):
            entries.append({
                "id": item.get("id"),
                "title": item.get("title") or "Untitled",
                "url": item.get("url"),
                "duration": item.get("duration")
            })
    return {"title": info.get("title") or "Playlist", "count": len(entries), "entries": entries}

def analyze(url):
    if not url or not url.strip():
        raise ValueError("Please enter a valid URL.")

    try:
        with YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True}) as ydl:
            info = ydl.extract_info(url.strip(), download=False)
    except Exception as e:
        raise RuntimeError(f"Unable to analyze this URL: {e}") from e

    formats = []
    seen = set()

    for f in info.get("formats", []):
        height = f.get("height")
        if not height or not f.get("format_id"):
            continue

        key = (height, f.get("ext"), f.get("vcodec"), f.get("acodec"))
        if key in seen:
            continue
        seen.add(key)

        formats.append({
            "format_id": f["format_id"],
            "height": height,
            "ext": f.get("ext", "unknown"),
            "vcodec": f.get("vcodec", "none"),
            "acodec": f.get("acodec", "none"),
            "filesize": _size(f.get("filesize") or f.get("filesize_approx")),
            "has_audio": f.get("acodec") not in (None, "none")
        })

    formats.sort(key=lambda x: (x["height"], x["has_audio"]), reverse=True)

    if not formats:
        raise RuntimeError("No downloadable video formats were found.")

    return {
        "id": info.get("id"),
        "title": info.get("title", "Unknown title"),
        "uploader": info.get("uploader") or info.get("channel") or "Unknown channel",
        "thumbnail": info.get("thumbnail"),
        "duration": _duration(info.get("duration")),
        "view_count": info.get("view_count"),
        "upload_date": info.get("upload_date"),
        "formats": formats,
    }

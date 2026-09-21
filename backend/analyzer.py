from yt_dlp import YoutubeDL

def analyze(url):
    if not url or not url.strip():
        raise ValueError("Please enter a valid URL.")

    opts = {"quiet": True, "no_warnings": True, "noplaylist": True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url.strip(), download=False)

    formats = []
    seen = set()

    for f in info.get("formats", []):
        height = f.get("height")
        if not height:
            continue
        key = (height, f.get("ext"), f.get("vcodec"), f.get("acodec"))
        if key in seen:
            continue
        seen.add(key)
        formats.append({
            "format_id": f.get("format_id"),
            "height": height,
            "ext": f.get("ext", "unknown"),
            "vcodec": f.get("vcodec", "none"),
            "acodec": f.get("acodec", "none"),
            "filesize": f.get("filesize") or f.get("filesize_approx"),
            "has_audio": f.get("acodec") not in (None, "none")
        })

    formats.sort(key=lambda x: (x["height"], x["has_audio"]), reverse=True)

    return {
        "id": info.get("id"),
        "title": info.get("title", "Unknown title"),
        "uploader": info.get("uploader") or info.get("channel") or "Unknown channel",
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "upload_date": info.get("upload_date"),
        "formats": formats,
    }

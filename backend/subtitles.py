def languages(info):
    return sorted((info.get("subtitles") or {}).keys())

def options(info):
    return sorted((info.get("automatic_captions") or {}).keys())

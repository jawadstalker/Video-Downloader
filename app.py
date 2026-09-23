from flask import Flask, render_template, request, jsonify
from backend.analyzer import analyze, analyze_playlist
from backend.queue import manager

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    media = None
    message = None
    url = request.form.get("url", "").strip()
    if request.method == "POST":
        try:
            media = analyze(url)
        except Exception as e:
            message = str(e) or "Unable to analyze the URL."
    return render_template("index.html", media=media, url=url, message=message, jobs=manager.all())

@app.post("/api/playlist")
def playlist():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url", "")).strip()
    try:
        return jsonify(analyze_playlist(url))
    except Exception as e:
        return jsonify({"error": str(e) or "Unable to analyze the playlist."}), 400

@app.post("/api/batch")
def batch():
    data = request.get_json(silent=True) or {}
    raw_urls = data.get("urls", [])
    if not isinstance(raw_urls, list):
        return jsonify({"error": "URLs must be provided as a list."}), 400

    urls = [str(u).strip() for u in raw_urls if str(u).strip()]
    format_id = str(data.get("format_id", "bestvideo+bestaudio/best")).strip()
    mode = str(data.get("mode", "video")).strip()
    audio_format = str(data.get("audio_format", "mp3")).strip()

    if not urls:
        return jsonify({"error": "No URLs provided."}), 400
    if mode not in {"video", "audio"}:
        return jsonify({"error": "Invalid download mode."}), 400
    if audio_format not in {"mp3", "m4a", "wav"}:
        return jsonify({"error": "Invalid audio format."}), 400

    return jsonify(manager.add_batch(urls, format_id, mode, audio_format))

@app.post("/download")
def download_route():
    url = request.form.get("url", "").strip()
    format_id = request.form.get("format_id", "").strip()
    mode = request.form.get("mode", "video").strip()
    audio_format = request.form.get("audio_format", "mp3").strip()

    if mode not in {"video", "audio"}:
        mode = "video"
    if audio_format not in {"mp3", "m4a", "wav"}:
        audio_format = "mp3"
    if not url or not format_id:
        return jsonify({"error": "URL and format are required."}), 400

    return jsonify(manager.add(url, format_id, mode, audio_format))

@app.get("/api/downloads")
def downloads():
    return jsonify(manager.all())

@app.post("/api/downloads/<job_id>/<action>")
def download_action(job_id, action):
    actions = {
        "pause": manager.pause,
        "resume": manager.resume,
        "cancel": manager.cancel,
        "retry": manager.retry,
    }
    fn = actions.get(action)
    if not fn:
        return jsonify({"error": "Invalid action."}), 400
    if not fn(job_id):
        return jsonify({"error": "Action is not available for this job."}), 409
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)

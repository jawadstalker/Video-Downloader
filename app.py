from flask import Flask, render_template, request, jsonify
from backend.analyzer import analyze
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

@app.route("/download", methods=["POST"])
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
    job = manager.add(url, format_id, mode, audio_format)
    return jsonify(job)

@app.get("/api/downloads")
def downloads():
    return jsonify(manager.all())

@app.post("/api/downloads/<job_id>/<action>")
def download_action(job_id, action):
    actions = {"pause": manager.pause, "resume": manager.resume,
               "cancel": manager.cancel, "retry": manager.retry}
    fn = actions.get(action)
    if not fn:
        return jsonify({"error": "Invalid action."}), 400
    if not fn(job_id):
        return jsonify({"error": "Action is not available for this job."}), 409
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)

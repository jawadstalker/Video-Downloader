from flask import Flask, render_template, request
from backend.analyzer import analyze
from backend.downloader import download

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
            message = str(e)

    return render_template("index.html", media=media, url=url, message=message)

@app.route("/download", methods=["POST"])
def download_route():
    url = request.form.get("url", "").strip()
    format_id = request.form.get("format_id", "").strip()
    mode = request.form.get("mode", "video").strip()
    audio_format = request.form.get("audio_format", "mp3").strip()

    try:
        download(url, format_id, mode, audio_format)
        return render_template(
            "index.html",
            media=None,
            url=url,
            message="Download completed. Check the downloads folder."
        )
    except Exception as e:
        return render_template(
            "index.html",
            media=None,
            url=url,
            message=f"Download failed: {e}"
        )

if __name__ == "__main__":
    app.run(debug=True)

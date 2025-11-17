from flask import Flask, render_template, request
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        ydl_opts_info = {"listformats": True}
        try:
            with YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])
                formats = [f for f in formats if f.get("height")]
        except Exception as e:
            return render_template("index.html", formats=None, message=f"Error: {e}")
        return render_template("index.html", formats=formats, url=url, message=None)
    return render_template("index.html", formats=None, message=None)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    format_id = request.form.get("format_id")

    ydl_opts_download = {
        "format": format_id,
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "video_%(height)sp.%(ext)s"),
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])
    except Exception as e:
        return render_template("index.html", formats=None, message=f"Download failed: {e}")

    return render_template("index.html", formats=None, message="Download completed! Check the 'downloads' folder.")

if __name__ == "__main__":
    app.run(debug=True)
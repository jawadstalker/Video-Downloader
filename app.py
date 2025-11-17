from flask import Flask, render_template, request
import video  # <-- اینجا کد video.py را وارد کردیم

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            formats = video.get_formats(url)
        except Exception as e:
            return render_template("index.html", formats=None, message=f"Error: {e}")
        return render_template("index.html", formats=formats, url=url, message=None)
    return render_template("index.html", formats=None, message=None)

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    format_id = request.form.get("format_id")
    try:
        video.download_video(url, format_id)
    except Exception as e:
        return render_template("index.html", formats=None, message=f"Download failed: {e}")
    return render_template("index.html", formats=None, message="Download completed! Check the 'downloads' folder.")

if __name__ == "__main__":
    app.run(debug=True)
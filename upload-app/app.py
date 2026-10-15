import os
from flask import Flask, request, send_from_directory, render_template_string
from werkzeug.utils import secure_filename

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB limit

PAGE = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>File Upload App</title>
<style>
body{font-family:Arial,sans-serif;background:#f4f7fb;padding:40px;text-align:center}
.box{background:#fff;max-width:520px;margin:auto;padding:30px;border-radius:12px;box-shadow:0 2px 8px #0002}
button{background:#ff9900;border:0;padding:10px 20px;border-radius:6px;font-weight:bold;cursor:pointer}
ul{text-align:left}
.msg{color:#0a7d2c;font-weight:bold}
</style></head><body><div class="box">
<h1>File Upload App</h1>
{% if message %}<p class="msg">{{ message }}</p>{% endif %}
<form method="post" enctype="multipart/form-data">
  <input type="file" name="file"> <button type="submit">Upload</button>
</form>
<h3>Uploaded files</h3>
<ul>{% for f in files %}<li><a href="/files/{{ f }}">{{ f }}</a></li>{% else %}<li>No files yet</li>{% endfor %}</ul>
</div></body></html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        f = request.files.get("file")
        if not f or f.filename == "":
            message = "Please choose a file first."
        else:
            name = secure_filename(f.filename)
            if not name:
                message = "Invalid file name."
            else:
                f.save(os.path.join(UPLOAD_DIR, name))
                message = "Uploaded: " + name
    files = sorted(os.listdir(UPLOAD_DIR))
    return render_template_string(PAGE, files=files, message=message)

@app.route("/files/<path:name>")
def download(name):
    return send_from_directory(UPLOAD_DIR, name)

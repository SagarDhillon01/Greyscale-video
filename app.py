import os
import uuid
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, flash, redirect, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
app.secret_key = "simple-grayscale-app"

MAX_VIDEO_SIZE_BYTES = 60 * 1024 * 1024
MAX_VIDEO_SIZE_MB = 60
app.config["MAX_CONTENT_LENGTH"] = MAX_VIDEO_SIZE_BYTES

UPLOAD_DIR = Path("/tmp/greyscale_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_video_size(uploaded_file) -> int:
    try:
        uploaded_file.stream.seek(0, os.SEEK_END)
        size = uploaded_file.stream.tell()
        uploaded_file.stream.seek(0)
        return size
    except (AttributeError, OSError):
        return uploaded_file.content_length or 0


def premium_message() -> str:
    return (
        f"This video exceeds the free {MAX_VIDEO_SIZE_MB} MB limit. "
        "Upgrade to the premium membership for ₹60 for 1 year to convert larger files."
    )


@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(_):
    flash(premium_message())
    return redirect(request.url)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "media" not in request.files or request.files["media"].filename == "":
            flash("Please choose a file.")
            return redirect(request.url)

        uploaded_file = request.files["media"]
        mime_type = uploaded_file.mimetype or ""
        file_size = get_video_size(uploaded_file)
        if file_size > MAX_VIDEO_SIZE_BYTES:
            flash(premium_message())
            return redirect(request.url)

        file_ext = Path(uploaded_file.filename).suffix.lower() or ".jpg"
        input_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{file_ext}"
        uploaded_file.save(input_path)

        if mime_type.startswith("video/"):
            output_path = UPLOAD_DIR / f"{input_path.stem}_gray.mp4"
            cap = cv2.VideoCapture(str(input_path))
            if not cap.isOpened():
                flash("Could not open the uploaded video.")
                return redirect(request.url)

            fps = cap.get(cv2.CAP_PROP_FPS) or 24
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
            if not out.isOpened():
                flash("Could not create the output video.")
                return redirect(request.url)

            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                out.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

            cap.release()
            out.release()
            return send_file(output_path, as_attachment=True, download_name=output_path.name)

        if mime_type.startswith("image/") or file_ext in {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"}:
            image = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
            if image is None:
                flash("Could not open the uploaded image.")
                return redirect(request.url)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            output_path = UPLOAD_DIR / f"{input_path.stem}_gray.jpg"
            success, encoded = cv2.imencode(".jpg", gray_image)
            if not success:
                flash("Could not create the grayscale image.")
                return redirect(request.url)

            output_path.write_bytes(encoded.tobytes())
            return send_file(output_path, as_attachment=True, download_name=output_path.name)

        flash("Please upload a valid image or video file.")
        return redirect(request.url)

    return render_template("index.html", max_video_size_mb=MAX_VIDEO_SIZE_MB)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

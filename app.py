
from flask import Flask, render_template, request, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

UPLOAD_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    if "medicalImage" not in request.files:
        return jsonify({"error": "Please select an image."}), 400

    file = request.files["medicalImage"]

    if file.filename == "":
        return jsonify({"error": "No image selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only JPG, JPEG and PNG images are allowed."}), 400

    filename = secure_filename(file.filename)
    file.save(UPLOAD_FOLDER / filename)

    return jsonify({
        "message": "Image received successfully by the backend.",
        "filename": filename
    }), 200


if __name__ == "__main__":
    app.run(debug=True)

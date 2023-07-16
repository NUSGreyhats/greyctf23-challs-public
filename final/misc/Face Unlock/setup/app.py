from flask import Flask, render_template, request, flash, redirect
from utils import extract_faces, load_valid_faces
import face_recognition
import os


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(512).hex())
FLAG = os.environ.get("FLAG", "greyctf{fake_flag}")
faces = load_valid_faces()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Get the image sent
    b64_img = request.form.get("img", None)

    if b64_img is None:
        return {"status": "error", "msg": "No image sent"}

    # Extract the faces
    face_encodings = extract_faces(b64_img)

    if len(face_encodings) > 1:
        return {
            "status": "error",
            "msg": f"Too many faces, detected {len(face_encodings)}",
        }

    if len(face_encodings) == 0:
        return {"status": "error", "msg": "No faces detected"}

    face_sent = face_encodings[0]
    results = face_recognition.compare_faces(faces, face_sent, tolerance=0.4)

    # Check if it is the correct face
    if any(results):
        return {"status": "success", "msg": f"This is your room access key: {FLAG}"}

    return {"status": "error", "msg": "Authentication failed."}


if __name__ == "__main__":
    app.run(debug=True)

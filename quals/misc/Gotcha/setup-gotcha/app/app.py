from flask import Flask, request, render_template, Response, redirect, session, flash, g
from flask.sessions import SessionMixin
from utils import generate_captcha, draw_captcha, convert_img_to_b64
import os
from time import time


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(512).hex())
FLAG = os.environ.get("FLAG", "grey{fake_flag}")
TIMEOUT = 120
STORE = {}


def reset(session: SessionMixin) -> None:
    now = time()
    expiry = now + TIMEOUT
    session["expiry"] = expiry
    session["score"] = 0
    return 0, expiry


def get_store():
    if "store" not in g:
        g.store = STORE
    return g.store


@app.route("/", methods=["GET"])
def index() -> Response:
    """Main page"""
    id = session.get("id", os.urandom(512).hex())
    score = session.get("score", 0)

    now = time()
    expiry = session.get("expiry", now + TIMEOUT)

    if expiry <= now:
        flash("Reset", "danger")
        score, expiry = reset(session)

    if score >= 100:
        flash(FLAG, "success")
        session["expiry"] = time() + TIMEOUT * 24 * 60 * 60

    captcha = generate_captcha()
    img = draw_captcha(captcha)
    b64_img = convert_img_to_b64(img)

    session["id"] = id
    session["img"] = b64_img
    session["score"] = score
    session["expiry"] = expiry

    get_store()[b64_img] = captcha

    return render_template("index.html", b64_img=b64_img, score=score, expiry=expiry)


@app.route("/submit", methods=["POST"])
def submit() -> Response:
    """Submit the captcha"""
    result = request.form.get("captcha", None)
    b64_img = session.get("img", None)
    score = session.get("score", 0)

    if result is not None and b64_img is not None:
        expected = get_store()[b64_img]
        if expected == result:
            session["score"] = score + 1
            flash("Congrats you got it right", "success")
        else:
            flash("Oh no, you got it wrong", "danger")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

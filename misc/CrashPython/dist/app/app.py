import os
import requests

from base64 import b64decode, b64encode
from flask import Flask, render_template, redirect, request, flash, Response
from constants import FLAG, ERROR, SUCCESS, JUDGE0_SUBMIT_URL, JUDGE0_BASE_URL, DECODE_KEYS, BANNED_WORDS


app = Flask(__name__)
app.secret_key = os.urandom(512).hex()


@app.route('/', methods=['GET', 'POST'])
def index() -> Response:
    """The main endpoint"""
    if request.method == 'GET':
        with open(__file__) as f:
            source_code = f.read()
        return render_template('index.html', banned_words=BANNED_WORDS, source_code=source_code)
    args = request.form
    code = args.get('code', '')

    if len(code) == 0:
        flash('Code cannot be empty', ERROR)
        return redirect('/')

    # Sanitize code
    code = sanitize(code)
    if len(code) == 0:
        return redirect('/')

    # Send to judge0
    token = send_code_to_execute(code)
    if len(token) == 0:
        flash('An unexpected error occurred', ERROR)
        return redirect('/')

    flash("Sucessfully sent", SUCCESS)
    return redirect(f"/view/{token}")


@app.route('/view/<path:path>', methods=['GET'])
def view_code(path: str) -> Response:
    """View the submitted code"""
    view_url = f'{JUDGE0_BASE_URL}/submissions/{path}/?base64_encoded=true'
    with requests.Session() as session:
        resp = session.get(view_url)
        data = resp.json()

    for key in DECODE_KEYS:
        if data.get(key, False):
            data[key] = b64decode(data[key]).decode()

    status = data.get('status', {}).get('id', 0)
    message = data.get('message', '')
    stderr = data.get('stderr', '')

    if status == 11 and message == "Exited with error status 139" and 'Segmentation fault' in stderr:
        flash(f"Congrats, you got the flag: {FLAG}!", SUCCESS)
    return render_template('results.html', **data)


def send_code_to_execute(code: str) -> str:
    """Send code to judge0 to execute"""
    b64_code = b64encode(code.encode()).decode()
    with requests.Session() as s:
        resp = s.post(JUDGE0_SUBMIT_URL, data={
            'source_code': b64_code,
            'language_id': 71,  # Python3
            'stdin': '',
        })
    return resp.json().get('token', '')


def sanitize(code: str) -> str:
    """Sanitize code"""
    for word in BANNED_WORDS:
        if word in code:
            flash(f'Banned word detected: "{word}"', ERROR)
            return ''
    return code


if __name__ == '__main__':
    app.run(debug=True)

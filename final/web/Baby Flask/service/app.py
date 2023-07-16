from flask import Flask, render_template_string, request, redirect, make_response
import jwt
from os import urandom
import re

secret = urandom(16)
app = Flask(__name__)

def generate_token(username):
    payload = {'username': username}
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

login_html = """
<form method="post" action="/login">
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" required>
    <br><br>
    <input type="submit" value="Login">
</form>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if all(
            i not in username for 
            i in "req url get sec".split()
            ) and re.match(r'^[(a-z|A-Z)+]+$', username):
            token = generate_token(username)
            response = make_response(redirect('/'))
            response.set_cookie('jwt', token)
            return response
    return login_html

@app.route('/')
def home():
    token = request.cookies.get('jwt')
    username = verify_token(token)
    if username:
        return render_template_string(f"""Welcome {{{{{username}}}}}!""")
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

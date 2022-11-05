import json
import os

import requests as requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required

from service.category_service import CategoryService
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
catService = CategoryService()
login_manager = LoginManager()
login_manager.init_app(app)

CLIENT_ID = 'deeg4tvrgziwwqpfwqtdd37z5gxltr'
CLIENT_SECRET = 'ifllbh3xvun6818en99t5b34jd90qv'
REDIRECT_URL = 'http://localhost:5000/callback'
AUTH_ENDPOINT = 'https://id.twitch.tv/oauth2/authorize'
TOKEN_ENDPOINT = 'https://id.twitch.tv/oauth2/token'
client = WebApplicationClient(CLIENT_ID)


@app.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('login'))


@app.route('/home')
def home():  # put application's code here
    return render_template('index.html', categories=catService.get_categories(), loggedIn=session.get('loggedIn'))


@app.route('/question')
def question_for_category():
    category = request.args.get('category')
    question = catService.question(category)
    return render_template('question.html', category=category, question=question)


@app.route('/answer', methods=['POST'])
def check_answer():
    if request.method == 'POST':
        question_id = request.json.get('question')
        given_answer = request.json.get('answer')
        return {'answer': catService.check_answer(question_id, given_answer)}
    return {'answer': None}


@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(str(client.prepare_request_uri(
        AUTH_ENDPOINT,
        redirect_uri='http://localhost:5000/callback',
        scope=["openid"],
    )))


class User:
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/callback', methods=['GET', 'POST'])
def login_callback():
    code = request.args.get("code")
    foo = TOKEN_ENDPOINT + '?client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET + '&code=' + code + '&grant_type=authorization_code' + '&redirect_uri=' + REDIRECT_URL
    print(foo)
    token_response = requests.post(foo)
    token = token_response.json()['access_token']
    # Parse the tokens!
    print(token_response.json())
    print(code)
    if token is not None:
        session['loggedIn'] = True;
        return redirect(url_for('home'))
    return "<h3>ERROR!!!!!!!!!</>"


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)

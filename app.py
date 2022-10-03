from flask import Flask, url_for, render_template, session, redirect
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

oauth = OAuth(app)

oauth.register(
    name='ma_cantine',
    client_id=f"{ os.getenv('CLIENT_ID') }",
    client_secret=f"{ os.getenv('CLIENT_SECRET') }",
    # must include the final slash in the URLs
    access_token_url=f"{ os.getenv('SERVICE_URL') }/o/token/",
    access_token_params=None,
    authorize_url=f"{ os.getenv('SERVICE_URL') }/o/authorize/",
    authorize_params=None,
    api_base_url=f"{ os.getenv('SERVICE_URL') }/",
    client_kwargs={'scope': 'user:read canteen:read canteen:write'},
)


@app.route('/')
def homepage():
    token = get_token(session)
    if token:
        return redirect('/profile')
    return render_template('home.html')


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.ma_cantine.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.ma_cantine.authorize_access_token()
    # would probably store token in a DB for a production app
    session['access_token'] = token.get('access_token')
    session['token_type'] = token.get('token_type')
    session['refresh_token'] = token.get('refresh_token')
    session['expires_at'] = token.get('expires_at')
    return redirect('/profile')


def get_token(session):
    if session.get('access_token'):
        return dict(
            access_token=session.get('access_token'),
            token_type=session.get('token_type'),
            refresh_token=session.get('refresh_token'),
            expires_at=session.get('expires_at'),
        )


@app.route('/profile')
def profile():
    token = get_token(session)
    if token:
        resp = oauth.ma_cantine.get('api/v1/userInfo/', token=token)
        resp.raise_for_status()
        profile = resp.json()
        resp = oauth.ma_cantine.get('api/v1/canteenPreviews/', token=token)
        resp.raise_for_status()
        previews = resp.json()
        return render_template('profile.html', profile=profile, previews=previews)
    else:
        return redirect('/')


# POST


@app.route('/logout')
def logout():
    session.pop('access_token'),
    session.pop('token_type'),
    session.pop('refresh_token'),
    session.pop('expires_at'),
    return redirect('/')

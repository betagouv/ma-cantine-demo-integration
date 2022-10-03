from flask import Flask
from flask import url_for, render_template, redirect
from flask import session, request
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


@app.route('/profile', methods=['GET'])
def profile():
    token = get_token(session)
    if token:
        # get user info
        resp = oauth.ma_cantine.get('api/v1/userInfo/', token=token)
        profile = resp.json()

        # get canteen previews
        resp = oauth.ma_cantine.get('api/v1/canteenPreviews/', token=token)
        previews = resp.json()

        # get first canteen and last year's diagnostic
        canteen = None
        year = 2021
        diagnostic = None
        if previews[0]:
            resp = oauth.ma_cantine.get(f"api/v1/canteens/{ previews[0]['id'] }", token=token)
            canteen = resp.json()
            # a diagnostic for last year might not already exist
            diagnostic = next(filter(lambda d: d['year'] == year, canteen['diagnostics']), None)

        return render_template('profile.html',
            profile=profile,
            previews=previews,
            canteen=canteen,
            diagnostic=diagnostic,
            year=year,
            status=request.args.get('status'),
            error=request.args.get('error')
        )
    else:
        return redirect('/')

@app.route('/profile', methods=['POST'])
def update_profile():
    token = get_token(session)
    if token:
        canteen_id = request.form['canteen_id']
        # update canteen
        resp = oauth.ma_cantine.patch(
            f"api/v1/canteens/{ canteen_id }",
            token=token,
            data={ 'name': request.form['canteen_name'] }
        )
        if resp.status_code < 300:
            # if canteen update was successful, continue to diagnostic create/update
            total = request.form['total']
            diagnostic_id = request.form.get('diagnostic_id', None)
            if diagnostic_id:
                # update diagnostic
                resp = oauth.ma_cantine.patch(
                    f"api/v1/canteens/{ canteen_id }/diagnostics/{ diagnostic_id }",
                    token=token,
                    # NB: you can provide the key in camelCase or snake_case
                    data={ 'value_total_ht': total }
                )
            elif total:
                # create diagnostic
                resp = oauth.ma_cantine.post(
                    f"api/v1/canteens/{ canteen_id }/diagnostics/",
                    token=token,
                    data={ 'valueTotalHt': total, 'year': request.form['year'] }
                )

        # update params with info of last API call
        params = f'?status={resp.status_code}'
        if resp.status_code >= 300:
            error = f'{resp.text}'
            params += f'&error={error}'
        return redirect(f'/profile{params}')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('access_token'),
    session.pop('token_type'),
    session.pop('refresh_token'),
    session.pop('expires_at'),
    return redirect('/')

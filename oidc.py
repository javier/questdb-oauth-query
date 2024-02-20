from flask import Flask, request, redirect, jsonify, session
import requests
import os

app = Flask(__name__)

# Load configuration variables into Flask's config
app.config['SECRET_KEY'] = os.getenv('FLASK_APP_SECRET_KEY', 'your_very_secret_key')
app.config['CLIENT_ID'] = os.getenv('FLASK_CLIENT_ID', 'test')
app.config['AUTHORIZATION_BASE_URL'] = os.getenv('FLASK_AUTHORIZATION_BASE_URL', 'https://pingfederate.whatever:9031/as/authorization.oauth2')
app.config['TOKEN_URL'] = os.getenv('FLASK_TOKEN_URL', 'https://pingfederate.whatever:9031/as/token.oauth2')
app.config['QUESTDB_URL'] = os.getenv('FLASK_QUESTDB_URL', 'https://questdbdemo.somewhere:9000/exec')
app.config['REDIRECT_URI'] = os.getenv('FLASK_REDIRECT_URI', 'http://localhost:9000')
app.config['PORT'] = os.getenv('FLASK_PORT', '9000')
app.config['SCOPE'] = ['openid']

tokens = {
    'access_token': None,
    'refresh_token': None
}

@app.route('/', methods=['GET'])
def main():
    code = request.args.get('code')
    if code:
        return handle_callback(code)
    else:
        return login()

def login():
    auth_url = f"{app.config['AUTHORIZATION_BASE_URL']}?response_type=code&client_id={app.config['CLIENT_ID']}&redirect_uri={app.config['REDIRECT_URI']}&scope={' '.join(app.config['SCOPE'])}"
    return redirect(auth_url)

def handle_callback(code):
    token_response = requests.post(app.config['TOKEN_URL'], data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': app.config['REDIRECT_URI'],
        'client_id': app.config['CLIENT_ID'],
    }, verify=True)

    token_json = token_response.json()
    if 'access_token' in token_json:
        tokens['access_token'] = token_json['access_token']
        tokens['refresh_token'] = token_json.get('refresh_token')
        if app.debug == True:
            print(tokens['access_token'])
        if 'original_query' in session:
            original_query = session.pop('original_query')
            return redirect(f"/query?query={original_query}")
        return 'OAuth flow completed. You can now use the /query endpoint.'
    else:
        error_description = token_json.get('error_description', 'No error description provided.')
        return f"Failed to obtain access token. Error description: {error_description}", 400

@app.route('/query')
def query():
    user_query = request.args.get('query')
    if not user_query:
        return 'No query provided', 400

    if 'access_token' not in tokens or tokens['access_token'] is None:
        session['original_query'] = user_query
        return redirect('/')

    headers = {'Authorization': f"Bearer {tokens['access_token']}"}
    params = {'query': user_query}
    response = requests.get(app.config['QUESTDB_URL'], headers=headers, params=params, verify=True)

    if response.status_code == 401:
        if 'refresh_token' in tokens and tokens['refresh_token']:
            refresh_access_token(tokens['refresh_token'])
            headers['Authorization'] = f"Bearer {tokens['access_token']}"
            response = requests.get(app.config['QUESTDB_URL'], headers=headers, params=params, verify=True)
            if response.status_code == 401:
                return redirect('/')
            return jsonify(response.json())
        else:
            return redirect('/')

    return jsonify(response.json())

def refresh_access_token(refresh_token):
    if app.debug == True:
        print("Refreshing access token")
    token_response = requests.post(app.config['TOKEN_URL'], data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': app.config['CLIENT_ID'],
    }, verify=True)

    token_json = token_response.json()
    tokens['access_token'] = token_json['access_token']
    tokens['refresh_token'] = token_json.get('refresh_token', refresh_token)
    if app.debug == True:
        print(tokens['access_token'])

if __name__ == "__main__":
    app.run(port=app.config['PORT'], debug=True)

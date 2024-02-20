# questdb-oauth-query: Flask Application for QuestDB OIDC/OAuth Authentication

This Flask application (`oidc.py`) is designed to authenticate with OIDC/OAuth and enable querying a QuestDB database, with
configuration via environment variables. It uses a refresh token to maintain the session
without requiring the user to re-authenticate frequently. Tokens are kept in-memory, so they are lost on restart.

## Security Note

**Important:** The application runs in debug mode by default, which prints the authentication token to the console upon
login or token refresh. While useful for debugging, this poses a security risk by exposing sensitive information. Exercise
caution and consider disabling debug mode in production environments.

## Setup

Before running the application, ensure that Python 3 and `pip` are installed on your system. It is recommended to use a
virtual environment for Python projects to avoid conflicts between project dependencies.

### Creating a Virtual Environment

#### Unix-like Systems (Linux, macOS)

```
python3 -m venv venv
source venv/bin/activate
```

#### Windows

Command Prompt:

```
python -m venv venv
venv\Scripts\activate.bat
```

PowerShell:

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Installing Dependencies

Install the required Python packages specified in `requirements.txt`:

```
pip install -r requirements.txt
```

## Configuration

Configure the application via the following environment variables, with defaults provided for ease of setup:

- `FLASK_APP_SECRET_KEY`: Secret key for Flask session management. Default: `'your_very_secret_key'`
- `FLASK_CLIENT_ID`: Client ID for OAuth authentication. Default: `'test'`
- `FLASK_AUTHORIZATION_BASE_URL`: OAuth authorization base URL. Default: `'https://pingfederate.whatever:9031/as/authorization.oauth2'`
- `FLASK_TOKEN_URL`: OAuth token URL. Default: `'https://pingfederate.whatever:9031/as/token.oauth2'`
- `FLASK_QUESTDB_URL`: QuestDB server URL. Default: `'https://questdbdemo.somewhere:9000/exec'`
- `FLASK_REDIRECT_URI`: Redirect URI for OAuth callback. Default: `'http://localhost:9000'`
- `PORT`: Port for the Flask application. Default: `9000`

## Available Endpoints

- **Root (`/`)**: Initiates the OAuth login process or handles the callback with an authorization code.
  - *No parameters required*. Automatically redirects to OAuth provider or the original query after successful authentication.

- **Login (`/login`)**: This endpoint is not directly accessible but is part of the OAuth flow initiated from the root.
  Redirects the user to the OAuth provider for authentication.

- **Query (`/query`)**: Allows querying the QuestDB database.
  - *Parameters*:
    - `query`: The SQL query to execute against the QuestDB database.

## Running the Application

### Unix-like Systems (Linux, macOS)

Set environment variables inline before executing `oidc.py`. Replace `<placeholder>` with actual values:

```
FLASK_APP_SECRET_KEY='<your_secret_key>' FLASK_CLIENT_ID='<your_client_id>'
FLASK_AUTHORIZATION_BASE_URL='<your_authorization_base_url>' FLASK_TOKEN_URL='<your_token_url>'
FLASK_QUESTDB_URL='<your_questdb_url>' FLASK_REDIRECT_URI='<your_redirect_uri>' PORT=9000 python oidc.py
```

### Windows

#### Command Prompt

Set the environment variables using the following command. Replace `<placeholder>` with actual values:

```
set FLASK_APP_SECRET_KEY=<your_secret_key> && set FLASK_CLIENT_ID=<your_client_id>
&& set FLASK_AUTHORIZATION_BASE_URL=<your_authorization_base_url> && set FLASK_TOKEN_URL=<your_token_url>
&& set FLASK_QUESTDB_URL=<your_questdb_url> && set FLASK_REDIRECT_URI=<your_redirect_uri>
&& set PORT=9000 && python oidc.py
```

#### PowerShell

Set environment variables inline in PowerShell. Ensure to replace `<placeholder>` with actual values:

```
$env:FLASK_APP_SECRET_KEY='<your_secret_key>'; $env:FLASK_CLIENT_ID='<your_client_id>';
$env:FLASK_AUTHORIZATION_BASE_URL='<your_authorization_base_url>'; $env:FLASK_TOKEN_URL='<your_token_url>';
$env:FLASK_QUESTDB_URL='<your_questdb_url>'; $env:FLASK_REDIRECT_URI='<your_redirect_uri>';
$env:PORT=9000; python oidc.py
```


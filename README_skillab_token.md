# Getting a Skillab Tracker session token

The Tracker API has no separate API key. You log in with the project username and password and receive a session token, which is sent with every later request. Your project client (`skillab_client.SkillabClient`) does this for you and prints "Authenticated successfully; token stored for session".

Base URL used in the project files: `https://skillab-tracker.csd.auth.gr/api`

## 1. Keep the credentials in `.env`

Project root, never in a report, a script or git (check that `.env` is in `.gitignore`):

```dotenv
SKILLAB_USERNAME=your username
SKILLAB_PASSWORD=your password
SKILLAB_API_BASE_URL=https://skillab-tracker.csd.auth.gr/api
```

## 2. Get the token

`POST <base URL>/login` with a JSON body holding the username and password. The answer is the token as plain text, in quotes.

Terminal (reads the values from `.env`):

```
set -a; source .env; set +a
```

```
curl -s -X POST "$SKILLAB_API_BASE_URL/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"username\": \"$SKILLAB_USERNAME\", \"password\": \"$SKILLAB_PASSWORD\"}"
```

Python (what the first project scripts did):

```python
import os, requests
r = requests.post(f"{os.environ['SKILLAB_API_BASE_URL']}/login",
                  json={"username": os.environ["SKILLAB_USERNAME"], "password": os.environ["SKILLAB_PASSWORD"]},
                  headers={"accept": "application/json", "Content-Type": "application/json"}, timeout=45)
r.raise_for_status()
token = r.text.replace('"', "")
```

## 3. Use the token

Send it as a header: `Authorization: Bearer <token>`. For example `POST <base URL>/jobs?page=1` with the filters in the body (`keywords`, `sources`, and the date filters your client uses, such as `min_upload_date`). Sources are listed by `GET <base URL>/jobs/sources`.

## Notes

- The token expires. After an authentication error or a 401, log in again.
- Queries without a source filter can hang on the large tables (first project scripts, `01_fetch_sample.py`). Filter by source or by date range, and keep the page count small.
- For the project data use `SkillabClient` (it handles the login and the retries). `diagnostics/113_skillab_keyword_probe.py` logs in on its own and only prints counts and titles for a few keywords.
- Whether the API website has an interactive page where you can log in and copy a token was not checked here. Ask the Skillab team for its address if you want one.

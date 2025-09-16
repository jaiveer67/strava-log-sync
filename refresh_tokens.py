import requests
import os
import time
from dotenv import load_dotenv

ENV_FILE = ".env"

load_dotenv()
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
EXPIRES_AT = int(os.getenv("STRAVA_EXPIRES_AT", "0"))

def refresh_strava_token():
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        }
    )
    new_tokens = response.json()
    update_env_file(new_tokens)
    return new_tokens

def update_env_file(tokens):
    with open(ENV_FILE, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("STRAVA_ACCESS_TOKEN="):
            new_lines.append(f"STRAVA_ACCESS_TOKEN={tokens['access_token']}\n")
        elif line.startswith("STRAVA_REFRESH_TOKEN="):
            new_lines.append(f"STRAVA_REFRESH_TOKEN={tokens['refresh_token']}\n")
        elif line.startswith("STRAVA_EXPIRES_AT="):
            new_lines.append(f"STRAVA_EXPIRES_AT={tokens['expires_at']}\n")
        else:
            new_lines.append(line)

    with open(ENV_FILE, "w") as f:
        f.writelines(new_lines)

def ensure_valid_token():
    if time.time() >= EXPIRES_AT:
        print("🔄 Refreshing expired Strava token...")
        refresh_strava_token()
    else:
        print("Strava token still valid.")

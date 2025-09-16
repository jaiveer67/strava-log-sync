import os
import requests
from dotenv import load_dotenv

load_dotenv()
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

def get_activities(since=None):
    """
    Fetches activities from Strava.
    If `since` is provided (as a UNIX timestamp), only activities after that time are returned.
    """
    load_dotenv(override=True)  # reload updated token
    STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"}
    params = {"per_page": 50}  # adjust if needed

    if since:
        params["after"] = since  # Strava expects UNIX timestamp (seconds)

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import datetime

load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def col_to_letter(col):
    """Convert 1-indexed column number to letter (1 -> A, 2 -> B, etc.)."""
    result = ""
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        result = chr(65 + remainder) + result
    return result

def get_month_tab_name(date_str):
    """Return the month tab name (e.g., 'September') for a given YYYY-MM-DD date."""
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%B")

def append_activity_to_sheet(activity):
    """Append a single Strava activity to the correct weekly block, skipping cells that already have data."""
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)

    date_str = activity["start_date_local"][:10]
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    month_tab = get_month_tab_name(date_str)

    # Determine week block
    first_week_row = 2
    rows_per_week = 6
    week_number = (dt.day - 1) // 7
    base_row = first_week_row + week_number * rows_per_week
    duration_row = base_row + 1
    distance_row = base_row + 2
    activity_name_row = base_row  # date range row

    # Determine column (Monday=2)
    col = dt.weekday() + 2
    col_letter = col_to_letter(col)

    duration = round(activity["moving_time"] / 60, 2)
    distance = round(activity["distance"] / 1000, 2)
    activity_name = activity.get("name", "")

    # Helper to check if a cell is empty
    def is_cell_empty(row):
        range_str = f"{month_tab}!{col_letter}{row}"
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range=range_str
        ).execute()
        values = result.get("values", [])
        if not values or not values[0] or values[0][0] == "":
            return True
        return False

    # Update Duration if empty
    if is_cell_empty(duration_row):
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f"{month_tab}!{col_letter}{duration_row}",
            valueInputOption="USER_ENTERED",
            body={"values": [[duration]]}
        ).execute()

    # Update Distance if empty
    if is_cell_empty(distance_row):
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f"{month_tab}!{col_letter}{distance_row}",
            valueInputOption="USER_ENTERED",
            body={"values": [[distance]]}
        ).execute()

    # Update Activity Name if empty
    if is_cell_empty(activity_name_row):
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f"{month_tab}!{col_letter}{activity_name_row}",
            valueInputOption="USER_ENTERED",
            body={"values": [[activity_name]]}
        ).execute()

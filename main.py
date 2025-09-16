from strava import get_activities
from sheets import append_activity_to_sheet, get_month_tab_name
from refresh_tokens import ensure_valid_token

def main():
    ensure_valid_token()

    # Fetch all recent activities from Strava
    activities = get_activities()

    synced_count = 0
    for activity in activities:
        append_activity_to_sheet(activity)
        synced_count += 1

    print(f"Synced {synced_count} activities!")

if __name__ == "__main__":
    main()

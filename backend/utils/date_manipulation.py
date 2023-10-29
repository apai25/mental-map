from datetime import datetime, timedelta

def get_first_day_of_week():
    # Get the current date
    today = datetime.now()

    # Calculate the difference in days between the current day of the week (0=Monday, 6=Sunday) and Monday (0)
    days_to_monday = today.weekday()

    # Subtract the difference to get the date of the first day of the week (Monday)
    first_day_of_week = today - timedelta(days=days_to_monday)

    # Format the date in "YYYY-MM-DD" format
    formatted_date = first_day_of_week.strftime("%Y-%m-%d")

    return formatted_date
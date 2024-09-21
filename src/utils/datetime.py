import time
from datetime import datetime, timedelta

def format_since_datetime(since): 
    if not isinstance(since, str) or len(since) <= 0:
        return None

    duration_mapping = {"h": "hours", "d": "days", "m": "months", "y": "years"}
    time_unit = since[-1]
    time_value = int(since[:-1])
    now = datetime.now()

    # Maybe some special case for today, yesterday

    if time_unit == "h":
        since_date = now - timedelta(hours=time_value)
    elif time_unit == "d":
        since_date = now - timedelta(days=time_value)
    elif time_unit == "m":
        since_date = now - timedelta(days=time_value * 30)
    elif time_unit == "y":
        since_date = now - timedelta(days=time_value * 365)

    return since_date.isoformat() + "Z"
        
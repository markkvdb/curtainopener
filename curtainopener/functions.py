from datetime import datetime, timedelta

def date_selector(hours, minutes):
    """Checks if alarm must be set for today or tomorrow."""
    timenow = datetime.now()
    if hours > timenow.hour.real:
        return timenow.strftime("%Y-%m-%d")
    else:
        if minutes > timenow.minute.real:
            return timenow.strftime("%Y-%m-%d")
        else:
            timenow += timedelta(days=1)
            return timenow.strftime("%Y-%m-%d")

def valid_time(hours, minutes):
    """Check if the selected time is valid, e.g. between 00:00 and 23:59."""
    if (hours <= 24 and hours >= 0):
        if (minutes == 0 and hours == 24) or ((minutes >= 0 and minutes <= 59) and hours != 24):
            return True

    return False


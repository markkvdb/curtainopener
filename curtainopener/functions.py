from datetime import datetime, timedelta
from .variables import variableDict

def date_selector(hours, minutes) -> str:
    """Checks if alarm must be set for today or tomorrow."""
    timenow = datetime.now()
    if hours > timenow.hour.real:
        return timenow.strftime("%Y-%m-%d")
    else:
        if minutes > timenow.minute.real and hours == timenow.hour.real:
            return timenow.strftime("%Y-%m-%d")
        else:
            timenow += timedelta(days=1)
            return timenow.strftime("%Y-%m-%d")

def valid_time(hours, minutes) -> bool:
    """Check if the selected time is valid, e.g. between 00:00 and 23:59."""
    if (hours <= 24 and hours >= 0):
        if (minutes == 0 and hours == 24) or ((minutes >= 0 and minutes <= 59) and hours != 24):
            return True

    return False

def seconds_till_execute(hours, minutes) -> int:
    """Calculate number of seconds till the job has to be started"""
    timenow = datetime.now()
    if hours > timenow.hour.real:
        seconds = (hours - timenow.hour.real) * 3600 + (minutes - timenow.minute.real) * 60
    else:
        if minutes > timenow.minute.real and hours == timenow.hour.real:
            seconds = (minutes - timenow.minute.real) * 60
        else:
            seconds = (24 - timenow.hour.real + hours) * 3600 + (minutes - timenow.minute.real) * 60

    return seconds

def curtain_job_controller_add(hours, minutes, open):
    global variableDict
    if variableDict['curtain_open'] == open:
        return

    seconds = seconds_till_execute(hours, minutes)

    variableDict['job_scheduler'].enter(2, 1, curtain_job, argument=(open,))
    variableDict['job_scheduler'].run()

def curtain_job(to_open):
    global variableDict
    # TODO create stepper controller
    if to_open:
        pass
    else:
        pass

    print("JOB EXECUTED!!!")
    variableDict['curtain_open'] = not variableDict['curtain_open']

from datetime import datetime, timedelta
from .variables import variableDict
from .alarm import Alarm


def valid_time(hours, minutes) -> bool:
    """Check if the selected time is valid, e.g. between 00:00 and 23:59."""
    if (hours <= 24 and hours >= 0):
        if (minutes == 0 and hours == 24) or ((minutes >= 0 and minutes <= 59) and hours != 24):
            return True

    return False


def curtain_job_controller_add(alarm):
    global variableDict
    if variableDict['curtain_open'] == alarm.open:
        return

    seconds = alarm.seconds_till_execute()

    variableDict['job_queue'].put((seconds, alarm))
    variableDict['event'].set()


def curtain_job(to_open):
    global variableDict

    # TODO create stepper controller
    if to_open:
        pass
    else:
        pass

    print("JOB EXECUTED!!!")
    variableDict['curtain_open'] = not variableDict['curtain_open']


def job_worker():
    global variableDict

    while True:
        # Wait for next job
        if variableDict['job_queue'].empty():
            variableDict['event'].wait()
        else:
            # TODO set time untill job correctly
            seconds_till_next_job = variableDict['job_queue'].queue[0][0]

            if seconds_till_next_job < 0:
                continue
            else:
                variableDict['event'].wait(seconds_till_next_job)

        # Execute job
        time, alarm = variableDict['job_queue'].get()
        curtain_job(alarm.open)

        # Set event back to False if queue is empty
        if variableDict['job_queue'].empty():
            variableDict['event'].clear()

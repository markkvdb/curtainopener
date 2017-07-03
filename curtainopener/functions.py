from flask import current_app
from .stepcontroller import motor_controller
from .database_handler import *
from .alarm import Alarm
from .variables import variableDict


def valid_time(hours, minutes) -> bool:
    """Check if the selected time is valid, e.g. between 00:00 and 23:59."""
    if (hours <= 24 and hours >= 0):
        if (minutes == 0 and hours == 24) or ((minutes >= 0 and minutes <= 59) and hours != 24):
            return True

    return False


def curtain_job_controller_add(alarm):
    global variableDict

    seconds = alarm.date.timestamp()

    variableDict['job_queue'].put((seconds, alarm))
    variableDict['event'].set()


def curtain_job(alarm):
    global variableDict

    if variableDict['curtain_open'] == alarm.open:
        return

    motor_controller(alarm)

    with app.app_context():
        db = get_db1(current_app)
        db.execute('update entries set done = 1 where id=?', (alarm.id,))
        db.commit()

    variableDict['curtain_open'] = not variableDict['curtain_open']


def job_worker():
    global variableDict

    while True:
        variableDict['event'].clear()

        # Wait for next job
        if variableDict['job_queue'].empty():
            variableDict['event'].wait()
            variableDict['event'].clear()

        while True:
            time, alarm = variableDict['job_queue'].queue[0]
            seconds_until_next_job = alarm.time_in_seconds()

            if seconds_until_next_job < 0:
                break

            variableDict['event'].wait(seconds_until_next_job)

        # Execute job
        time, alarm = variableDict['job_queue'].get()
        curtain_job(alarm)

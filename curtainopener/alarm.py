from datetime import datetime, timedelta


class Alarm(object):

    def __init__(self, hours, minutes, open):
        self.hours = hours
        self.minutes = minutes
        self.open = open
        self.date = self.date_selector()

    def date_selector(self):
        """Checks if alarm must be set for today or tomorrow."""
        time_now = datetime.now()
        if self.hours <= time_now.hour.real:
            if self.minutes > time_now.minute.real and self.hours == time_now.hour.real:
                pass
            else:
                time_now += timedelta(days=1)

        time_now.replace(hour=self.hours, minute=self.minutes, second=0)
        return time_now

    def date_to_str(self) -> str:
        return self.date.strftime("%Y-%m-%d")

    def seconds_till_execute(self) -> int:
        """Calculate number of seconds till the job has to be started"""
        timenow = datetime.now()
        if self.hours > timenow.hour.real:
            seconds = (self.hours - timenow.hour.real) * 3600 + (self.minutes - timenow.minute.real) * 60
        else:
            if self.minutes > timenow.minute.real and self.hours == timenow.hour.real:
                seconds = (self.minutes - timenow.minute.real) * 60
            else:
                seconds = (24 - timenow.hour.real + self.hours) * 3600 + (self.minutes - timenow.minute.real) * 60

        return seconds

    # TODO give time in seconds for the queue
    def time_in_seconds(self):
        pass

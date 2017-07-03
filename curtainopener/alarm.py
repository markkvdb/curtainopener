from datetime import datetime, timedelta


class Alarm(object):

    def __init__(self, hours, minutes, open, seconds_to_last):
        self.id = -1
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.open = open
        self.seconds_to_last = seconds_to_last

        self.date = self.date_selector()

    def set_id(self, id):
        self.id = id

    def date_selector(self):
        """Checks if alarm must be set for today or tomorrow."""
        time_now = datetime.now()
        if self.hours <= time_now.hour.real:
            if self.minutes > time_now.minute.real and self.hours == time_now.hour.real:
                pass
            else:
                time_now += timedelta(days=1)

        time_now1 = time_now.replace(hour=self.hours, minute=self.minutes, second=0)
        time_now1 -= timedelta(seconds=self.seconds_to_last)

        return time_now1

    def date_to_str(self) -> str:
        return self.date.strftime("%Y-%m-%d %H:%M:%S")


    def time_in_seconds(self) -> int:
        timedelta_alarm = self.date - datetime.now()
        return timedelta_alarm.total_seconds()

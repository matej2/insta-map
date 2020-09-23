from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta
from datetime import datetime
import random


class RandomIntervalTrigger(IntervalTrigger):
    min_minutes = 1

    def __init__(self, weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, end_date=None, timezone=None,
                 jitter=None):
        # Saving the parameters
        self.__weeks = weeks
        self.__days = days
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds

        # Creating the random parameters
        weeks = random.randint(1, weeks) if weeks != 0 else weeks
        days = random.randint(1, days) if days != 0 else days
        hours = random.randint(1, hours) if hours != 0 else hours
        minutes = random.randint(1, minutes) if minutes != 0 else minutes
        seconds = random.randint(1, seconds) if seconds != 0 else seconds

        # Initializating the trigger
        super().__init__(weeks, days, hours, minutes, seconds, start_date, end_date, timezone, jitter)

    def get_next_fire_time(self, previous_fire_time: datetime, now: datetime):
        # Creating the random parameters
        weeks = random.randint(1, self.__weeks) if self.__weeks != 0 else self.__weeks
        days = random.randint(1, self.__days) if self.__days != 0 else self.__days
        hours = random.randint(1, self.__hours) if self.__hours != 0 else self.__hours
        minutes = random.randint(1, self.__minutes) if self.__minutes != 0 else self.__minutes
        seconds = random.randint(1, self.__seconds) if self.__seconds != 0 else self.__seconds

        # Generating the new scheduling time
        offset = timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours, weeks=weeks)

        if previous_fire_time is None:
            previous_fire_time = now

        new_time = previous_fire_time + offset

        return new_time

import calendar
import datetime
import functools
import time
import traceback

from findtime.day import Day
from findtime import errors
from findtime import parsing
from findtime import utils
from findtime import validation


YEAR = datetime.datetime.today().year
DAYS_THIS_YEAR = 366 if calendar.isleap(YEAR) else 365


class Pattern(object):

    def __init__(self, day_map=None):
        if not day_map:
            day_map = {}
        self.day_map = {
            day: day_obj
            for (day, day_obj) in day_map.items()
            if day_obj
        }

    @staticmethod
    def load(times, weekdays=None, real_days=None):
        if real_days:
            (start, end) = real_days
            real_days = range(start, end + 1)
        else:
            real_days = range(1, 365 + 1 + 1)  # leap days

        times = times
        weekdays = frozenset(weekdays) if weekdays else frozenset()
        filtered_days = [
            utils.day_of_year(day)
            for day in
            [datetime.datetime.strptime("{}/{}".format(YEAR, day), "%Y/%j") for day in real_days]
            if day.weekday() in weekdays
        ]

        return Pattern(day_map={day: Day.load([times]) for day in filtered_days})

    def __getitem__(self, key):
        return self.day_map.get(key)

    def __or__(self, other):
        return Pattern(day_map={
            real_day: (self[real_day] | other[real_day])
            for real_day in (frozenset(self) | frozenset(other))
        })

    def __and__(self, other):
        return Pattern(day_map={
            real_day: (self[real_day] & other[real_day])
            for real_day in (frozenset(self) & frozenset(other))
        })

    def __invert__(self):
        return Pattern(day_map={
            day: (~self[day] if day in self else ~Day())
            for day in range(DAYS_THIS_YEAR)
        })

    def __iter__(self):
        return iter(self.day_map.keys())

    def __repr__(self):
        return "<Pattern: {} days>".format(len(self.day_map))

    def show(self):
        for i in range(min(self), max(self) + 1):
            print("{}: {}".format(i, self[i]))


def parse(pattern_string):
    (dates, pattern_string) = parsing.parse_date(pattern_string)
    (days, pattern_string) = parsing.parse_days(pattern_string)
    times = parsing.parse_times(pattern_string)

    if dates:
        dates = validation.validate_dates(*dates)
    if days:
        days = validation.validate_days(days)
    times = validation.validate_times(*times)

    return (dates, days, times)


def parse_named_schedule(named_schedule):
    print("named_schedule: '{}'".format(named_schedule))

    try:
        (title, schedule_string) = named_schedule.split(': ', 1)
    except ValueError:
        print("ERROR! No colon-space between title and schedule in: '{}'".format(named_schedule))
        return

    title = title.strip()
    schedule_string = schedule_string.strip()

    print("Title: '{}'".format(title))
    print("schedule_string: '{}'".format(schedule_string))

    pattern = Pattern()
    dates = days = times = None
    for (i, pattern_string) in enumerate(schedule_string.split(), 1):
        print("pattern_string {}: '{}'".format(i, pattern_string))
        try:
            parsed = parse(pattern_string)
        except errors.Error as err:
            print(err)
            raise err

        if parsed[0]:
            dates = parsed[0]
        if parsed[1]:
            days = parsed[1]
        times = parsed[2]

        pattern |= Pattern.load(times, weekdays=days, real_days=dates)

    return pattern


def free_time(*patterns):
    return functools.reduce(lambda a, b: a & b, patterns)


SEAN = "Sean: T6-9p MWR1:35-2:40p WF11:45-1:25 R12-1p"
NICK = "Nick: MRFSU5:30-6:30ap"
ELISE = "Elise: M6-10ap T6-8ap W8-11ap RF6-p"
MATT = "Matt S17 (busy):  MWR10:30-11:30a 1:35-2:40p MR11:45-1:25 4:35-5:40p M2:50-4:30p W2:50-5:10p"
NAT = "Nat S17 (busy):  MWF9-9:50a TR9:40-10:55a 12:30-1:45 MW10:25-11:15a 12:30-1:45 2-3:15p W3:25-4:40p"


# parse_named_schedule("x")
# parse_named_schedule("Matt's schedule:  4/12-29M-R9-5ap S10-6")
t0 = time.time()
# p1 = parse_named_schedule("Example:  4/12-29M-R9-5 WS7-7:30p")
# p2 = parse_named_schedule("Test: T-F9:30-5:30 8-2")
p1 = ~parse_named_schedule(MATT)
p2 = ~parse_named_schedule(NAT)
pi = free_time(p1, p2)
t1 = time.time()

print(p1)
# p1.show()
print()

print(p2)
# p2.show()
print()

print(pi)
pi.show()
print()

print(t1 - t0)

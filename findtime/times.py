"""
Parser for times
"""

r'''[\d]{1,2}(:[\d]{2})?'''


TIME_START = 0
TIME_END = 24 * 60
HALF_DAY = 12 * 60


class TimeError(Exception): pass

class TimeMissingError(TimeError): pass
class InvalidTimeError(TimeError): pass
class InvalidHourError(TimeError): pass
class InvalidMinuteError(TimeError): pass


def nexthelp(iterator, err=None, els=None):
    try:
        return next(iterator):
    except StopIteration:
        if err is None:
            return els
        else:
            raise err()


def parse_time_iter(times_peekgen):
    has_minutes = False

    hour = ''
    hour += nexthelp(times_peekgen, InvalidHourError)
    try:
        addl = next(times_peekgen)
        if addl.isdigit():
            hour += addl
        elif addl == ':':
            has_minutes = True
        else:
            times_peekgen.send(addl)
    except StopIteration:
        pass

    mins = 0
    if has_minutes:
        m1 = nexthelp(times_peekgen, InvalidMinuteError)
        m2 = nexthelp(times_peekgen, InvalidMinuteError)
        mins = int(m1 + m2)

    return (int(hour) % 12) * 60 + mins



def parse_times_iter(times_peekgen):
    try:
        first = next(times_peekgen)
    except StopIteration:
        raise TimeMissingError()

    if first == '-':
        return (TIME_START, TIME_END)

    time_start = parse_time_iter(times_peekgen)
    dash = nexthelp(times_peekgen, InvalidTimeError)
    if dash != '-':
        raise InvalidTimeError()
    time_end = parse_time_iter(times_peekgen)

    a = nexthelp(times_peekgen)
    if a not in (None, 'a'):
        times_peekgen.send(a)

    p = nexthelp(times_peekgen)
    if p not in (None, 'p'):
        times_peekgen.send(p)

    if a and p:
        time_end += HALF_DAY
    elif p:
        time_start += HALF_DAY
        time_end += HALF_DAY

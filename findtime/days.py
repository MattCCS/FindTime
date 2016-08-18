"""
Parser for days!
"""

from findtime import peekgen


WILDCARD = '*'
DAYS_ORDERED = list("MTWRFSU")
DAYS = dict(zip(DAYS_ORDERED, xrange(7)))


class DayError(Exception): pass

class DaysMissingError(DayError): pass
class DuplicateDaysError(DayError): pass
class InvalidDayError(DayError): pass
class InvalidDayRangeError(DayError): pass
class NonMonotonicDaysError(DayError): pass
class NonMonotonicDayRangeError(DayError): pass


def day_range_inclusive(start, end):
    DAYS_REVERSED = {v: k for (k, v) in DAYS.items()}
    return [DAYS_REVERSED[i] for i in xrange(DAYS[start], DAYS[end] + 1)]


def parse_days_iter(days_peekgen):
    try:
        first = next(days_peekgen)
    except StopIteration:
        raise DaysMissingError()

    if first == WILDCARD:
        return DAYS_ORDERED
    elif first not in DAYS:
        raise InvalidDayError()

    valid_days = set(DAYS) | set('-')
    days = [first]
    for maybe_day in days_peekgen:
        if maybe_day in valid_days:
            days.append(maybe_day)
        else:
            days_peekgen.send(maybe_day)  # we must have reached the end!
            break

    if '-' in days:
        if len(days) != 3:
            raise InvalidDayRangeError()
        (start, end) = (days[0], days[2])
        if start not in DAYS or end not in DAYS:
            raise InvalidDayRangeError()
        if DAYS[start] >= DAYS[end]:
            raise NonMonotonicDayRangeError()
        return day_range_inclusive(start, end)

    if len(set(days)) < len(days):
        raise DuplicateDaysError()

    nums = [DAYS[day] for day in days]
    if sorted(nums) != nums:
        raise NonMonotonicDaysError()

    return days

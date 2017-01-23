
import re

from findtime import constants
from findtime import errors


TIME_REGEX = r'''(?P<h>[\d]{1,2})(:(?P<m>[\d]{2}))?$'''
PERIOD_REGEX = r'''(a)?(p)?$'''

DAYS_REGEX = r'''([MTWRFSU]{1,7})'''
DAY_RANGE_REGEX = r'''((?P<start>[MTWRFSU])-(?P<end>[MTWRFSU]))'''
DAY_WILDCARD = r'''(\*)'''

DATE_REGEX = r'''(?P<m1>[1-9]\d?)/(?P<d1>[1-9]\d?)-((?P<m2>[1-9]\d?)/)?(?P<d2>[1-9]\d?)'''


def day_range_inclusive(start, end):
    # if not constants.DAYS[start] < constants.DAYS[end]:
    #     raise errors.BadDayRangeError("Start day does not come before end!")
    # return [constants.DAYS_REVERSED[i] for i in range(constants.DAYS[start], constants.DAYS[end] + 1)]
    start_i = constants.DAYS[start]
    end_i = constants.DAYS[end]
    delta = abs(end_i - start_i)
    return [constants.DAYS_REVERSED[i % 7] for i in range(start_i, start_i + delta)]


def parse_date(pattern_string):
    m = re.match(DATE_REGEX, pattern_string)
    if not m:
        return (None, pattern_string)

    m1 = m.group('m1')
    d1 = m.group('d1')
    m2 = m.group('m2')
    d2 = m.group('d2')

    dates = ((m1, d1), (m2, d2))

    return (dates, pattern_string[m.end():])


def parse_days(pattern_string):
    m = re.match(DAY_WILDCARD, pattern_string)
    if m:
        return (constants.DAYS, pattern_string[m.end():])

    m = re.match(DAY_RANGE_REGEX, pattern_string)
    if m:
        start = m.group('start')
        end = m.group('end')
        return (day_range_inclusive(start, end), pattern_string[m.end():])

    m = re.match(DAYS_REGEX, pattern_string)
    if m:
        return (list(m.group()), pattern_string[m.end():])

    return (None, pattern_string)


def parse_time(time_string):
    m = re.match(TIME_REGEX, time_string)
    if not m:
        raise errors.BadTimeError(time_string)
    hr = m.group('h')
    mi = m.group('m')
    return int(hr) * 60 + (int(mi) if mi else 0)


def parse_times(pattern_string):
    try:
        (start, end) = pattern_string.split('-', 1)
    except ValueError:
        raise errors.NoTimesError(pattern_string)

    end_cut = end.rstrip('ap')
    assert len(end_cut) >= (len(end) - 2)
    ap = end[len(end_cut):]
    m = re.match(PERIOD_REGEX, ap)
    if not m:
        raise errors.BadPeriodError(pattern_string)
    (a, p) = m.groups()

    start = parse_time(start)
    end = parse_time(end_cut)

    return (start, end, a, p)

"""
"""

DAYS = frozenset("MTWRFSU")
PERIODS = frozenset("ap")

class DaysParseError(Exception): pass
class PatternParseError(Exception): pass


def parse_days(days):
    days_set = frozenset(days)
    if not days_set <= DAYS:
        raise DaysParseError("Days '{}' not subset of valid days '{}'!".format(days, DAYS))
    return days_set


def convert_time(time, period='a'):
    if ':' in time:
        (h, m) = map(int, time.split(':'))
        val = 60 * h + m
    elif not time:
        return -1
    else:
        h = int(time)
        val = 60 * h

    return val + (0 if period == 'a' else 60 * 12)


def parse_timerange(timerange):

    times = timerange.rstrip('ap').split('-')

    # grab/infer start and end periods
    if timerange.endswith('ap'):
        periods = ('a', 'p')
    elif timerange.endswith('a'):
        periods = ('a', 'a')
    elif timerange.endswith('p'):
        periods = ('p', 'p')
    else:
        (abs_start, abs_end) = map(convert_time, times)
        if abs_start < abs_end:
            periods = ('a', 'a')
        else:
            periods = ('a', 'p')

    # validate start and end periods
    start = convert_time(times[0], periods[0])
    end = convert_time(times[1], periods[1])

    if start == -1:
        start = 0
    if end == -1:
        end = 60 * 24 - 1

    print (start, end)
    if start > end:
        print "[!] Start time cannot be after end time!"
    elif start == end:
        print "[!] Start and end time cannot be the same!"


def parse_timeranges(timeranges):
    return map(parse_timerange, timeranges.split(','))


def parse_pattern(pattern):
    day_start = next((i for (i, c) in enumerate(pattern) if c.upper() in DAYS), -1)
    if day_start < 0:
        raise PatternParseError("No day found!")
    # print day_start

    day_end = len(pattern) - next((i for (i, c) in enumerate(reversed(pattern)) if c.upper() in DAYS), -1)
    # print day_end

    dates = pattern[:day_start]
    days = pattern[day_start:day_end]
    timeranges = pattern[day_end:]
    parse_timeranges(timeranges)

    return (dates, days, timeranges)


def parse_schedule(schedule):
    patterns = schedule.split(' ')
    return map(parse_pattern, patterns)

pattern_1 = "1/1-4/5M-R8-10p"
pattern_2 = "7/11-12/30M-F9-5"
pattern_3 = "M-F7-9a,5-6p"
pattern_4 = "M-F9-5p"
pattern_5 = "M1-2,1-2a,1-2p,1-2ap"

schedule_1 = "M-F6:30-p S10- U12-8p"
schedule_2 = "M- T-R- F-8p S-11"

for p in [pattern_1, pattern_2, pattern_3, pattern_4, pattern_5]:
    print p
    print parse_pattern(p)
    print

print schedule_1
print parse_schedule(schedule_1)
print

print schedule_2
print parse_schedule(schedule_2)
print

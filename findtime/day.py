
import collections
import functools


HALF_DAY = 12 * 60
WHOLE_DAY = 24 * 60 - 1


def minutes_to_hhmm(minutes):
    (h, m) = divmod(minutes, 60)
    h = (h - 1) % 12 + 1
    return "{}:{:>02}{}m".format(h, m, 'a' if minutes < HALF_DAY else 'p')


def pair_up(iterable):
    iterable = list(iterable)
    return list(zip(iterable, iterable[1:]))[::2]


class Day(object):

    def __init__(self, flagged_times=None):
        if not flagged_times:
            flagged_times = []
        self.flagged_times = list(flagged_times)
        for (_, flag) in self.flagged_times:
            assert flag in (True, False)

    @staticmethod
    def load(times):
        flagged = []
        for (start, end) in times:
            assert start < end
            flagged_time = ((start, True), (end, False))
            flagged.append(flagged_time)
        return functools.reduce(lambda a, b: a | b, map(Day, flagged), Day())

    @staticmethod
    def iterate(flagged_a, flagged_b, threshold):
        """Must not self-overlap"""
        assert threshold in (1, 2)

        if not flagged_a:
            flagged_a = []
        if not flagged_b:
            flagged_b = []

        counts = collections.defaultdict(int)
        for (time, flag) in (flagged_a + flagged_b):
            counts[time] += (1 if flag else -1)

        flags = 0
        for (time, delta) in sorted(counts.items()):
            if flags < threshold <= flags + delta:
                yield (time, True)
            elif flags + delta < threshold <= flags:
                yield (time, False)
            flags += delta

    @staticmethod
    def invert(flagged):
        entire_day = [(0, True), (WHOLE_DAY, False)]

        counts = collections.defaultdict(int)
        for (time, flag) in (flagged + entire_day):
            counts[time] += (1 if flag else -1)

        flags = 0
        for (time, delta) in sorted(counts.items()):
            if flags != 1 and flags + delta == 1:
                yield (time, True)
            elif flags == 1 and flags + delta != 1:
                yield (time, False)
            flags += delta

    def __or__(self, other):
        other = other if other else []
        return Day(Day.iterate(list(self), list(other), 1))

    def __ror__(self, other):
        return self | other

    def __and__(self, other):
        other = other if other else []
        return Day(Day.iterate(list(self), list(other), 2))

    def __rand__(self, other):
        return self & other

    def __invert__(self):
        return Day(Day.invert(list(self)))

    def __iter__(self):
        return iter(self.flagged_times)

    def __bool__(self):
        return bool(self.flagged_times)

    def __repr__(self):
        ranges = ', '.join(
            "{}-{}".format(minutes_to_hhmm(start), minutes_to_hhmm(end))
            for ((start, _), (end, _)) in pair_up(self)
        )
        return "<Day: {}>".format(ranges)

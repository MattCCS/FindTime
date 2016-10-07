
import datetime

import constants
import errors
import utils


HALF_DAY = 12 * 60
FULL_DAY = HALF_DAY * 2


def validate_times(start, end, am, pm):
    (ds, de) = (0, 0)

    if am and pm:
        de = HALF_DAY
    elif am:
        pass
    elif pm:
        ds = HALF_DAY
        de = HALF_DAY
    if not am and not pm:
        if not start >= end:
            raise errors.TimeValidationError("Time range ambiguous!")
        de = HALF_DAY

    start += ds
    end += de

    if not start < end:
        raise errors.TimeValidationError("Time start is not < end!")
    if not 0 <= start < FULL_DAY:
        raise errors.TimeValidationError("Start is not in 24-hour range!")
    if not 0 <= end < FULL_DAY:
        raise errors.TimeValidationError("End is not in 24-hour range!")

    return (start, end)


def validate_days(days):
    indices = [constants.DAYS[day] for day in days]

    if not len(set(indices)) == len(indices):
        raise errors.DayValidationError("Duplicate days!")

    # if not sorted(indices) == indices:
    #     raise errors.DayValidationError("Days not monotonic!")

    return list(sorted(indices))


def validate_dates(date_start, date_end):
    (m1, d1) = date_start
    (m2, d2) = date_end
    if not m2:
        m2 = m1

    form = "%Y/%m/%d"
    year = datetime.datetime.now().year

    if not d1:
        date_1 = datetime.datetime.strptime("{}/1/1".format(year), form)
    else:
        try:
            date_1 = datetime.datetime.strptime("{}/{}/{}".format(year, m1, d1), form)
        except ValueError:
            raise errors.DateValidationError("Start date didn't parse!")

    if not d2:
        date_2 = datetime.datetime.strptime("{}/12/31".format(year), form)
    else:
        try:
            date_2 = datetime.datetime.strptime("{}/{}/{}".format(year, m2, d2), form)
        except ValueError:
            raise errors.DateValidationError("End date didn't parse!")

    return (utils.day_of_year(date_1), utils.day_of_year(date_2))


import unittest

from findtime import days
from findtime import peekgen


class TestDays(unittest.TestCase):

    def evaluate(self, test_days):
        return days.parse_days_iter(peekgen.peekgen(test_days))

    def test_no_days(self):
        with self.assertRaises(days.DaysMissingError):
            self.evaluate('')

    def test_wildcard(self):
        self.assertListEqual(list('MTWRFSU'), self.evaluate('-'))

    def test_good_day(self):
        self.assertListEqual(list('M'), self.evaluate('M'))

    def test_good_days(self):
        self.assertListEqual(list('MTW'), self.evaluate('MTW'))

    def test_no_runover_days(self):
        self.assertListEqual(list('MTW'), self.evaluate('MTW9-5'))

    def test_late_wildcard_ends_early_days(self):
        self.assertListEqual(list('MTW'), self.evaluate('MTW-'))

    def test_duplicates(self):
        with self.assertRaises(days.DuplicateDaysError):
            self.evaluate('MM')

    def test_non_monotonic(self):
        with self.assertRaises(days.NonMonotonicDaysError):
            self.evaluate('FM')

    def test_non_monotonic_range(self):
        with self.assertRaises(days.NonMonotonicDayRangeError):
            self.evaluate('F-M')

    def test_non_monotonic_range_same_day(self):
        with self.assertRaises(days.NonMonotonicDayRangeError):
            self.evaluate('M-M')

    def test_short_range(self):
        with self.assertRaises(days.InvalidDayRangeError):
            self.evaluate('M-')

    def test_range_bad_start(self):
        with self.assertRaises(days.InvalidDayRangeError):
            self.evaluate('M--')

    def test_good_range(self):
        self.assertListEqual(list('MTWRF'), self.evaluate('M-F'))

    def test_no_runover_range(self):
        self.assertListEqual(list('MTWRF'), self.evaluate('M-F9-5'))

    def test_no_runover_half_range(self):
        self.assertListEqual(list('MTWRF'), self.evaluate('M-F-5p'))

    def test_late_wildcard_ends_early_range(self):
        self.assertListEqual(list('MTWRF'), self.evaluate('M-F*'))


if __name__ == '__main__':
    unittest.main()

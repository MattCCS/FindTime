
import unittest

from findtime import days
from findtime import peekgen


class TestDays(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.TIME = '9-5'

    def evaluate(self, test_days):
        return days.parse_days_iter(peekgen.peekgen(test_days))

    def test_good_range(self):
        self.assertListEqual(list('MTWRF'), self.evaluate('M-F'))

    def test_no_run_over(self):
        self.assertListEqual(list('MTWRF'), self.evaluate('M-F9-5'))

    def test_bad_range(self):
        with self.assertRaises(days.NonMonotonicDayRangeError):
            self.evaluate('F-M')


if __name__ == '__main__':
    unittest.main()

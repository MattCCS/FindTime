
import unittest

from findtime import times
from findtime import peekgen


class TestTimes(unittest.TestCase):

    def evaluate(self, test_days):
        # return days.parse_days_iter(peekgen.peekgen(test_days))
        pass

    # def test_no_days(self):
    #     with self.assertRaises(days.DaysMissingError):
    #         self.evaluate('')

    # def test_wildcard(self):
    #     self.assertListEqual(list('MTWRFSU'), self.evaluate('*'))


if __name__ == '__main__':
    unittest.main()

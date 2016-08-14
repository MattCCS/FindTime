
import unittest

from findtime import days


class TestDays(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.GARBAGE = 'hello'

    def test_days(self):

        TEST_TIME = 'hello'
        TEST_DAYS = [
            '',
        ]

        for test_days in TEST_DAYS:
            test_days = test_days + TEST_TIME
            test_days_peekgen = peekgen.peekgen(test_days)
            print parse_days_iter(test_days_peekgen)
            print list(test_days_peekgen)


if __name__ == '__main__':
    unittest.main()

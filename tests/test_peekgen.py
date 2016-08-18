
import unittest

from findtime import peekgen


class TestDays(unittest.TestCase):

    def test_peekgen_empty(self):
        peek = peekgen.peekgen('')
        with self.assertRaises(StopIteration):
            next(peek)

    def test_peekgen_one(self):
        peek = peekgen.peekgen('a')
        self.assertEqual('a', next(peek))

    def test_peekgen_multiple(self):
        peek = peekgen.peekgen('abc')
        self.assertListEqual(list('abc'), list(peek))

    def test_peekgen_insert(self):
        peek = peekgen.peekgen('abc')
        next(peek)
        peek.send(1)
        self.assertEqual(1, next(peek))
        self.assertListEqual(list('bc'), list(peek))

    def test_peekgen_insert_multiple(self):
        peek = peekgen.peekgen('abcd')
        next(peek)
        peek.send(1)
        self.assertEqual(1, next(peek))
        self.assertEqual('b', next(peek))
        self.assertEqual('c', next(peek))
        peek.send(2)
        self.assertEqual(2, next(peek))
        self.assertListEqual(list('d'), list(peek))


if __name__ == '__main__':
    unittest.main()

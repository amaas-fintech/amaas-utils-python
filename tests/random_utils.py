from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import date
from decimal import Decimal
import unittest

from amaasutils.random_utils import random_string, random_decimal, random_date


class RandomUtilsTest(unittest.TestCase):

    def test_RandomString(self):
        test_string = random_string(6)
        self.assertEqual(len(test_string), 6)
        test_string = random_string(8)
        self.assertEqual(len(test_string), 8)

    def test_RandomDate(self):
        test_date = random_date(start_year=2005, end_year=2005)
        self.assertEqual(type(test_date), date)
        self.assertEqual(test_date.year, 2005)

    def test_RandomDecimal(self):
        test_decimal = random_decimal()
        self.assertEqual(type(test_decimal), Decimal)
        self.assertGreater(test_decimal, 0)
        self.assertLess(test_decimal, 100)

if __name__ == '__main__':
    unittest.main()

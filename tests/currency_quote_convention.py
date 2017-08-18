from __future__ import absolute_import, division, print_function, unicode_literals

from amaasutils.currency_quote_convention import check_cross, get_currency_quote_convention

import unittest


class CurrencyQuoteConventionTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_GetCurrencyQuoteConvention(self):
        self.assertEqual('EURUSD', get_currency_quote_convention('EUR'))
        self.assertEqual('USDCNY', get_currency_quote_convention('CNY'))
        self.assertEqual(None, get_currency_quote_convention('ABC'))

    def test_CheckCross(self):
        self.assertTrue(check_cross('USDEUR'))
        self.assertTrue(check_cross('CNYSGD'))
        self.assertFalse(check_cross('EURUSD'))
        
from __future__ import absolute_import, division, print_function, unicode_literals

from amaasutils.currency_countrycode_mapping import currency_to_countrycode, countrycode_to_currency

import unittest

class CurrencyCountryCodeMappingTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CurrencyToCountryCode(self):
        self.assertEqual('SGP', currency_to_countrycode('SGD'))
        self.assertEqual(None, currency_to_countrycode('HELLO'))

    def test_CountryCodeToCurrency(self):
        self.assertEqual('SGD', countrycode_to_currency('SGP'))
        self.assertEqual(None, countrycode_to_currency('Heaven'))
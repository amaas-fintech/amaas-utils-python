from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime, date
import unittest

from amaasutils.param_utils import param_to_array, param_to_boolean, param_to_datetime, str_to_bool


class ParamUtilsTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.search_params = {'single': 'a_string', 'multiple': 'many,strings,in,a,row',
                              'single_int': '123', 'multiple_ints': '1,2,3',
                              'boolean': 'true', 'datetime': '2015-3-03 13:00'}

    def test_StrToBook(self):
        test_str = 'TRUE'
        self.assertEqual(str_to_bool(test_str), True)
        test_str = 'tRuE'
        self.assertEqual(str_to_bool(test_str), True)
        test_str = 'fAlSe'
        self.assertEqual(str_to_bool(test_str), False)
        test_str = 'TEST'
        self.assertEqual(str_to_bool(test_str), None)

    def test_ParamToArray(self):
        single_result = param_to_array(param_name='single', search_params=self.search_params)
        self.assertEqual(single_result, ['a_string'])
        multiple_results = param_to_array(param_name='multiple', search_params=self.search_params)
        self.assertEqual(multiple_results, ['many', 'strings', 'in', 'a', 'row'])

    def test_ParamToArrayTypeCasting(self):
        single_int_result = param_to_array(param_name='single_int', search_params=self.search_params,
                                           value_type=int)
        self.assertEqual(single_int_result, [123])
        multiple_int_results = param_to_array(param_name='multiple_ints', search_params=self.search_params,
                                              value_type=int)
        self.assertEqual(multiple_int_results, [1, 2, 3])

    def test_ParamToArrayMissing(self):
        result = param_to_array(param_name='missing', search_params=self.search_params)
        self.assertEqual(result, [])

    def test_ParamToArrayMissingSearchParams(self):
        result = param_to_array(param_name='single', search_params=None)
        self.assertEqual(result, None)

    def test_ParamToBoolean(self):
        param = param_to_boolean(param_name='boolean', search_params=self.search_params)
        self.assertEqual(param, True)

    def test_ParamToBooleanMissing(self):
        param = param_to_boolean(param_name='missing', search_params=self.search_params)
        self.assertEqual(param, None)

    def test_ParamToDatetime(self):
        param = param_to_datetime(param_name='datetime', search_params=self.search_params)
        self.assertEqual(param, datetime(2015, 3, 3, 13, 0))

    def test_ParamToDatetimeDateOnly(self):
        param = param_to_datetime(param_name='datetime', search_params=self.search_params, date_only=True)
        self.assertEqual(param, date(2015, 3, 3))

    def test_ParamToDatetimeMissing(self):
        param = param_to_datetime(param_name='missing', search_params=self.search_params)
        self.assertEqual(param, None)

if __name__ == '__main__':
    unittest.main()

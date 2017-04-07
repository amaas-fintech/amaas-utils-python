from __future__ import absolute_import, division, print_function, unicode_literals

import json
import unittest

from amaasutils.case import to_snake_case, dict_camel_to_snake_case, dict_snake_to_camel_case


class CaseTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_ToSnakeCase(self):
        input_str = 'inputString'
        self.assertEqual(to_snake_case(input_str), 'input_string')

    def test_JsonCamelToSnakeCase(self):
        test_input = {'fieldOne': 'valueOne', 'fieldTwo': 'value_two',
                      'fieldThree': {'fieldThreeOne': 'valueThreeOne',
                                     'fieldThreeTwo': 'value_three_two'}}
        test_json = json.loads(json.dumps(test_input))  # Convert to JSON formatting
        test_output = dict_camel_to_snake_case(test_json, convert_subkeys=True)
        expected_output = {'field_one': 'valueOne', 'field_two': 'value_two',
                           'field_three': {'field_three_one': 'valueThreeOne',
                                           'field_three_two': 'value_three_two'}}
        self.assertEqual(test_output, expected_output)

    def test_JsonSnakeToCamelCase(self):
        test_input = {'field_one': 'valueOne', 'field_two': 'value_two',
                      'field_three': {'field_three_one': 'valueThreeOne',
                                      'field_three_two': 'value_three_two'}}
        test_json = json.loads(json.dumps(test_input))  # Convert to JSON formatting
        test_output = dict_snake_to_camel_case(test_json, convert_subkeys=True)
        expected_output = {'fieldOne': 'valueOne', 'fieldTwo': 'value_two',
                           'fieldThree': {'fieldThreeOne': 'valueThreeOne',
                                          'fieldThreeTwo': 'value_three_two'}}
        self.assertEqual(test_output, expected_output)

    def test_KeyedChildrenCamelToSnakeCase(self):
        test_input = {'fieldOne': 'valueOne', 'fieldTwo': 'value_two',
                      'fieldThree': {'KeyOne': {'fieldThreeOneOne': 'valueThreeOne',
                                                'fieldThreeOneTwo': 'value_three_two'},
                                     'key_two': {'fieldThreeTwoOne': 'valueThreeOne',
                                                 'fieldThreeTwoTwo': 'value_three_two'},
                                     'keyThree': [{'fieldThreeThreeOneOne': 'valueThreeThreeOneOne',
                                                   'fieldThreeThreeOneTwo': 'value_three_three_one_two'},
                                                  {'fieldThreeThreeTwoOne': 'valueThreeThreeTwoOne',
                                                   'fieldThreeThreeTwoTwo': 'value_three_three_two_two'}]}}
        test_json = json.loads(json.dumps(test_input))  # Convert to JSON formatting
        test_output = dict_camel_to_snake_case(test_json)
        expected_output = {'field_one': 'valueOne', 'field_two': 'value_two',
                           'field_three': {'KeyOne': {'field_three_one_one': 'valueThreeOne',
                                                      'field_three_one_two': 'value_three_two'},
                                           'key_two':
                                               {'field_three_two_one': 'valueThreeOne',
                                                'field_three_two_two': 'value_three_two'},
                                           'keyThree': [{'field_three_three_one_one': 'valueThreeThreeOneOne',
                                                         'field_three_three_one_two': 'value_three_three_one_two'},
                                                        {'field_three_three_two_one': 'valueThreeThreeTwoOne',
                                                         'field_three_three_two_two': 'value_three_three_two_two'}]}}
        self.assertEqual(test_output, expected_output)

    def test_KeyedChildrenSnakeToCamelCase(self):
        test_input = {'field_one': 'valueOne', 'field_two': 'value_two',
                      'field_three': {'KeyOne': {'field_three_one_one': 'valueThreeOneOne',
                                                 'field_three_one_two': 'value_three_one_two'},
                                      'key_two': {'field_three_two_one': 'valueThreeTwoOne',
                                                  'field_three_two_two': 'value_three_two_two'},
                                      'keyThree': [{'field_three_three_one_one': 'valueThreeThreeOneOne',
                                                    'field_three_three_one_two': 'value_three_three_one_two'},
                                                   {'field_three_three_two_one': 'valueThreeThreeTwoOne',
                                                    'field_three_three_two_two': 'value_three_three_two_two'}]}}
        test_json = json.loads(json.dumps(test_input))  # Convert to JSON formatting
        test_output = dict_snake_to_camel_case(test_json)
        expected_output = {'fieldOne': 'valueOne', 'fieldTwo': 'value_two',
                           'fieldThree': {'KeyOne': {'fieldThreeOneOne': 'valueThreeOneOne',
                                                     'fieldThreeOneTwo': 'value_three_one_two'},
                                          'key_two': {'fieldThreeTwoOne': 'valueThreeTwoOne',
                                                      'fieldThreeTwoTwo': 'value_three_two_two'},
                                          'keyThree': [{'fieldThreeThreeOneOne': 'valueThreeThreeOneOne',
                                                        'fieldThreeThreeOneTwo': 'value_three_three_one_two'},
                                                       {'fieldThreeThreeTwoOne': 'valueThreeThreeTwoOne',
                                                        'fieldThreeThreeTwoTwo': 'value_three_three_two_two'}]}}
        self.assertEqual(test_output, expected_output)

if __name__ == '__main__':
    unittest.main()

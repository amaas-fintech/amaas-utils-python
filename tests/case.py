from __future__ import absolute_import, division, print_function, unicode_literals

import json
import unittest

from amaasutils.case import to_snake_case, dict_camel_to_snake_case, dict_snake_to_camel_case


class CaseTest(unittest.TestCase):

    def test_ToSnakeCase(self):
        input_str = 'inputString'
        self.assertEqual(to_snake_case(input_str), 'input_string')

    def test_JsonCamelToSnakeCase(self):
        test_input = {'fieldOne': 'valueOne', 'fieldTwo': 'value_two',
                      'fieldThree': {'fieldThreeOne': 'valueThreeOne',
                                     'fieldThreeTwo': 'value_three_two'}}
        test_json = json.loads(json.dumps(test_input)) # Convert to JSON formatting
        test_output = dict_camel_to_snake_case(test_json)
        expected_output = {'field_one': 'valueOne', 'field_two': 'value_two',
                           'field_three': {'field_three_one': u'valueThreeOne',
                                           'field_three_two': u'value_three_two'}}
        self.assertEqual(test_output, expected_output)

    def test_JsonSnakeToCamelCase(self):
        test_input = {'field_one': 'valueOne', 'field_two': 'value_two',
                      'field_three': {'field_three_one': u'valueThreeOne',
                                      'field_three_two': u'value_three_two'}}
        test_json = json.loads(json.dumps(test_input)) # Convert to JSON formatting
        test_output = dict_snake_to_camel_case(test_json)
        expected_output = {'fieldOne': 'valueOne', 'fieldTwo': 'value_two',
                           'fieldThree': {'fieldThreeOne': u'valueThreeOne',
                                          'fieldThreeTwo': u'value_three_two'}}
        self.assertEqual(test_output, expected_output)

if __name__ == '__main__':
    unittest.main()

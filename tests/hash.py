from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from amaasutils.hash import compute_hash


class HashTest(unittest.TestCase):
    
    def setUp(self):
        self.attributes = {'field_one': 'value_one',
                           'dict_field': {'dict_field_one': 'dict_field_value'},
                           'nested_field': {'dict_field': {'dict_field_one': 'dict_field_value'}}}

    def test_Field(self):
        test_attribute = self.attributes.copy()
        expected_hashcode = compute_hash(self.attributes)
        hashcode = compute_hash(test_attribute)
        self.assertEqual(hashcode, expected_hashcode)

        test_attribute = self.attributes.copy()
        test_attribute['field_one'] = 'updated_value'
        new_hashcode = compute_hash(test_attribute)
        self.assertNotEqual(hashcode, new_hashcode)

    def test_dictField(self):
        test_attribute = self.attributes.copy()
        hashcode = compute_hash(test_attribute)
        test_attribute['dict_field']['new_dict_field'] = 'new_value'
        new_hashcode = compute_hash(test_attribute)
        self.assertNotEqual(hashcode, new_hashcode)

    
    def test_nestedDictField(self):
        test_attribute = self.attributes.copy()
        hashcode = compute_hash(test_attribute)
        test_attribute['nested_field']['dict_field']['dict_field_two'] = 'updated_value'
        new_hashcode = compute_hash(test_attribute)
        self.assertNotEqual(hashcode, new_hashcode)
   

if __name__ == '__main__':
    unittest.main()

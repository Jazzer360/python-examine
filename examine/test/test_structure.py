import unittest
from examine import Structure

class TestStructure(unittest.TestCase):

    def test_non_structure(self):
        astr = 'string'
        expected = '=== str ==='
        actual = str(Structure(astr))
        self.assertEqual(actual, expected)

    def test_simple_list(self):
        alist = [1, 2, 3]
        expected = '=== [int] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_none_list(self):
        alist = [None, None, None]
        expected = '=== [NoneType] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_mixed_type_list(self):
        alist = [1, 'string', {'key': 'val'}]
        expected = '=== [<mixed-type>] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_simple_dict(self):
        adict = {'key1': 'val1'}
        expected = ('=== dict ===\n'
                    'key1 - str')
        actual = str(Structure(adict))
        self.assertEqual(actual, expected)

    def test_dict_with_lists(self):
        adict = {'list1': [1, 2, 3], 'list2': ['a', 'b', 'c']}
        expected = ('=== dict ===\n'
                    'list1 - [int]\n'
                    'list2 - [str]')
        actual = str(Structure(adict))
        self.assertEqual(actual, expected)

    def test_nonuniform_dicts_in_list(self):
        alist = [{'key1': 'val1', 'key2': 'val2'},
                 {'key1': 'val1', 'key3': 'val3'}]
        expected = ('=== [dict] ===\n'
                    'key1 - str\n'
                    '*key2 - str\n'
                    '*key3 - str')
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_blank_list_in_dict(self):
        adict = {'list': []}
        expected = ('=== dict ===\n'
                    'list - []')
        actual = str(Structure(adict))
        self.assertEqual(actual, expected)

    def test_blank_list(self):
        alist = []
        expected = '=== [] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_blank_dict(self):
        adict = {}
        expected = '=== dict ==='
        actual = str(Structure(adict))
        self.assertEqual(actual, expected)

    def test_defer_list_type_if_empty(self):
        alist = [{'list': [1, 2, 3]}, {'list': []}]
        expected = ('=== [dict] ===\n'
                    'list - [int]')
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_empty_list_merged_with_non_list(self):
        alist = [{'list': []}, {'list': 'str'}]
        expected = ('=== [dict] ===\n'
                    'list - <mixed-type>')
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_nested_list(self):
        alist = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9]]]
        expected = '=== [[[int]]] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_incosistent_list_depth(self):
        alist = [[1, 2, 3], [[4, 5, 6], [7, 8, 9]]]
        expected = '=== [<mixed-type>] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_merging_none_list_with_int_list(self):
        alist = [[1, 2, 3], [None]]
        expected = '=== [[*int]] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_nested_dict(self):
        adict = {'l1': {'l2': {'l3': 'val'}}}
        expected = ('=== dict ===\n'
                    'l1 - dict\n'
                    '  l2 - dict\n'
                    '    l3 - str')
        actual = str(Structure(adict))
        self.assertEqual(actual, expected)

    def test_add_empty_list_to_list_of_dicts(self):
        alist = [{'key1': [{'subkey1': 'subval1', 'subkey2': 'subval2'}]},
                 {'key1': [{'subkey1': 'subval1'}]},
                 {'key1': []}]
        expected = ('=== [dict] ===\n'
                    'key1 - [dict]\n'
                    '  subkey1 - str\n'
                    '  *subkey2 - str')
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_none_in_list(self):
        alist = [1, 2, 3, None]
        expected = '=== [*int] ==='
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)

    def test_none_as_val_of_key_in_list_of_dicts(self):
        alist = [{'key': 'val'}, {'key': None}]
        expected = ('=== [dict] ===\n'
                    'key - *str')
        actual = str(Structure(alist))
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
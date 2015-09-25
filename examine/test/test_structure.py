import unittest
from ..examine import Structure

class TestStructure(unittest.TestCase):

    def assertChildren(self, structure):
        for child in structure.children:
            self.assertIs(child.parent, structure)
            self.assertChildren(child)

    def test_non_structure(self):
        astr = 'string'
        expected = '=== str ==='
        struc = Structure(astr)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_simple_list(self):
        alist = [1, 2, 3]
        expected = '=== [int] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_none_list(self):
        alist = [None, None, None]
        expected = '=== [NoneType] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_mixed_type_list(self):
        alist = [1, 'string', {'key': 'val'}]
        expected = '=== [<mixed-type>] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_simple_dict(self):
        adict = {'key1': 'val1'}
        expected = ('=== dict ===\n'
                    'key1 - str')
        struc = Structure(adict)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_dict_with_lists(self):
        adict = {'list1': [1, 2, 3], 'list2': ['a', 'b', 'c']}
        expected = ('=== dict ===\n'
                    'list1 - [int]\n'
                    'list2 - [str]')
        struc = Structure(adict)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_nonuniform_dicts_in_list(self):
        alist = [{'key1': 'val1', 'key2': 'val2'},
                 {'key1': 'val1', 'key3': 'val3'}]
        expected = ('=== [dict] ===\n'
                    'key1 - str\n'
                    '*key2 - str\n'
                    '*key3 - str')
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_blank_list_in_dict(self):
        adict = {'list': []}
        expected = ('=== dict ===\n'
                    'list - []')
        struc = Structure(adict)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_blank_list(self):
        alist = []
        expected = '=== [] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_blank_dict(self):
        adict = {}
        expected = '=== dict ==='
        struc = Structure(adict)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_defer_list_type_if_empty(self):
        alist = [{'list': [1, 2, 3]}, {'list': []}]
        expected = ('=== [dict] ===\n'
                    'list - [int]')
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_empty_list_merged_with_non_list(self):
        alist = [{'list': []}, {'list': 'str'}]
        expected = ('=== [dict] ===\n'
                    'list - <mixed-type>')
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_nested_list(self):
        alist = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9]]]
        expected = '=== [[[int]]] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_incosistent_list_depth(self):
        alist = [[1, 2, 3], [[4, 5, 6], [7, 8, 9]]]
        expected = '=== [[<mixed-type>]] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_merging_none_list_with_int_list(self):
        alist = [[None], [1, 2, 3], [4, 5, 6], [None]]
        expected = '=== [[*int]] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_nested_dict(self):
        adict = {'l1': {'l2': {'l3': 'val'}}}
        expected = ('=== dict ===\n'
                    'l1 - dict\n'
                    '  l2 - dict\n'
                    '    l3 - str')
        struc = Structure(adict)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_add_empty_list_to_list_of_dicts(self):
        alist = [{'key1': [{'subkey1': 'subval1', 'subkey2': 'subval2'}]},
                 {'key1': []},
                 {'key1': [{'subkey1': 'subval1'}]}]
        expected = ('=== [dict] ===\n'
                    'key1 - [dict]\n'
                    '  subkey1 - str\n'
                    '  *subkey2 - str')
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_none_in_list(self):
        alist = [1, 2, 3, None]
        expected = '=== [*int] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_none_as_val_of_key_in_list_of_dicts(self):
        alist = [{'key': 'val'}, {'key': None}]
        expected = ('=== [dict] ===\n'
                    'key - *str')
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_tuple(self):
        atuple = ('string', 1)
        expected = '=== (str, int) ==='
        struc = Structure(atuple)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_deep_list_nest(self):
        alist = [[[1],[]],[[],[1]], None, []]
        expected = '=== [*[[int]]] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_list_of_tuples(self):
        alist = [('str', None, []), ('str', 1, 2, 'over')]
        expected = '=== [(str, *int, <mixed-type>, *str)] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)

    def test_empty_tuple_merging(self):
        alist = [tuple(), ('str', 1)]
        expected = '=== [(*str, *int)] ==='
        struc = Structure(alist)
        self.assertEqual(str(struc), expected)
        self.assertChildren(struc)
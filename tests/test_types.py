import unittest
from conjure_python.essence_types import EssenceMatrix, EssenceFunction, EssenceRelation, EssenceRecord, EssenceSequence, EssenceTuple, EssenceSet

class TestEssenceObjects(unittest.TestCase):

    def test_essence_matrix(self):
        essence_json_matrix = {
                '1': {'1': 1, '2': 1, '3': 1, '4': 1, '5': 2, '6': 2, '7': 2, '8': 2},
                '2': {'1': 1, '2': 1, '3': 2, '4': 2, '5': 1, '6': 1, '7': 2, '8': 2},
                '3': {'1': 1, '2': 2, '3': 1, '4': 2, '5': 1, '6': 2, '7': 1, '8': 2},
                '4': {'1': 1, '2': 2, '3': 2, '4': 1, '5': 2, '6': 1, '7': 1, '8': 2}
            }
        matrix = EssenceMatrix(
            essence_json_matrix,
            "matrix indexed by [int(1..k), int(1..b)] of int(1..g)"
        )
        # Test basic properties
        self.assertEqual(matrix.index_types, (int, int))
        self.assertEqual(matrix.shape, (4, 8))
        self.assertEqual(matrix[1][4], 1)
        
        # Test different access methods
        self.assertEqual(matrix[3, 1], 1)
        
        # Test iteration
        matrix_rows = list(matrix)
        self.assertEqual(len(matrix_rows), 4)
        
        # Verify all values match original data
        for row_idx, row in enumerate(matrix, 1):
            for col_idx, value in enumerate(row, 1):
                self.assertEqual(value, int(essence_json_matrix[str(row_idx)][str(col_idx)]))
        
        # Test specific values from original data
        for k, v in essence_json_matrix['3'].items():
            self.assertEqual(matrix[3, int(k)], v)
        
        # Test length
        self.assertEqual(len(matrix), 4)
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(matrix), int))

    def test_essence_function(self):
        essence_json_func = {
            "1": 1, "2": 4, "3": 7, "4": 15, "5": 3, "6": 16, "7": 2, "8": 10, "9": 8,
            "10": 15, "11": 1, "12": 13, "13": 2, "14": 15, "15": 8, "16": 9, "17": 2,
            "18": 17, "19": 3, "20": 15
        }
        func = EssenceFunction(essence_json_func, "function (total) int(1..n_cars) --> int(1..n_cars)")
        
        # Test domain and codomain sets
        self.assertEqual(func.domain_values, set(int(k) for k in essence_json_func.keys()))
        self.assertEqual(func.codomain_values, set(int(v) for v in essence_json_func.values()))
        
        # Test function call behavior
        for k, v in essence_json_func.items():
            self.assertEqual(func(int(k)), int(v))
        
        # Test iteration
        items_count = 0
        for k, v in func:
            items_count += 1
            self.assertEqual(func(k), v)
        self.assertEqual(items_count, len(essence_json_func))
        
        # Test length
        self.assertEqual(len(func), len(essence_json_func))
        
        # Test string representation
        str_repr = str(func)
        self.assertTrue(isinstance(str_repr, str))
        self.assertTrue(len(str_repr) > 0)
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(func), int))
        
        # Test type parsing
        self.assertEqual(func.types['domain'], int)
        self.assertEqual(func.types['codomain'], int)

    def test_essence_relation(self):
        essence_json_relation = [[1, 1], [1, 2], [1, 5], [2, 1], [2, 2], [2, 4]]
        relation = EssenceRelation(
            essence_json_relation,
            "relation (minSize 1) of ( int(1..n_classes) * int(1..n_options) )"
        )
        
        # Test basic properties
        self.assertEqual(relation.relations_len, 2)
        self.assertEqual(relation.relation_type, (int, int))
        
        # Test element access
        for i, el in enumerate(relation):
            self.assertEqual(tuple(int(v) for v in essence_json_relation[i]), el)
        
        # Test direct indexing
        self.assertEqual(relation[0], (1, 1))
        self.assertEqual(relation[2], (1, 5))
        
        # Test tuple indexing
        self.assertEqual(relation[0, 0], 1)
        self.assertEqual(relation[2, 1], 5)
        
        # Test length
        self.assertEqual(len(relation), len(essence_json_relation))
        
        # Test iteration
        relations_count = 0
        for rel in relation:
            relations_count += 1
            self.assertEqual(len(rel), 2)
        self.assertEqual(relations_count, len(essence_json_relation))
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(relation), int))
        
        # Test string representation
        str_repr = str(relation)
        self.assertTrue(isinstance(str_repr, str))
        self.assertTrue(len(str_repr) > 0)

    def test_essence_record(self):
        record_data = {"A": 0, "B": 1}
        record = EssenceRecord(record_data, 'record {A : int(0..1), B : int(1..2)}')
        
        # Test basic properties
        self.assertEqual(list(record.keys()), ["A", "B"])
        self.assertEqual(list(record.values()), [0, 1])
        self.assertEqual(record["A"], 0)
        self.assertEqual(record["B"], 1)
        
        # Test items method
        items = list(record.items())
        self.assertEqual(len(items), 2)
        self.assertEqual(dict(items), record_data)
        
        # Test iteration
        values = []
        for value in record:
            values.append(value)
        self.assertEqual(values, [0, 1])
        
        # Test length
        self.assertEqual(len(record), 2)
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(record), int))
        
        # Test string representation
        str_repr = str(record)
        self.assertTrue(isinstance(str_repr, str))
        self.assertTrue("A: 0" in str_repr)
        self.assertTrue("B: 1" in str_repr)

    def test_essence_tuple(self):
        tuple_data = [1, 9, 1]
        essence_tuple = EssenceTuple(tuple_data, "tuple(int(1..5), int(9..15), int(1..5))")
        
        # Test values
        self.assertEqual(essence_tuple.values, tuple(tuple_data))
        
        # Test indexing
        self.assertEqual(essence_tuple[0], 1)
        self.assertEqual(essence_tuple[1], 9)
        self.assertEqual(essence_tuple[2], 1)
        
        # Test iteration
        items = []
        for item in essence_tuple:
            items.append(item)
        self.assertEqual(items, tuple_data)
        
        # Test length
        self.assertEqual(len(essence_tuple), 3)
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(essence_tuple), int))
        
        # Test string representation
        str_repr = str(essence_tuple)
        self.assertEqual(str_repr, "(1, 9, 1)")
        
        # Test types
        self.assertEqual(essence_tuple.types, [int, int, int])

    def test_complex_tuple(self):
        # Testing a more complex tuple with mixed types
        tuple_data = [False, 10, True]
        essence_tuple = EssenceTuple(tuple_data, "tuple(bool, int(1..15), bool)")
        
        self.assertEqual(essence_tuple.values, (False, 10, True))
        self.assertEqual(essence_tuple.types, [bool, int, bool])

    def test_essence_set(self):
        # Testing a set with integer elements
        set_data = [9, 10, 11, 12, 13]
        essence_set = EssenceSet(set_data, "find S: set (size 5) of int(9..16)")
        
        # Test basic properties
        self.assertEqual(essence_set.domain_type, int)
        self.assertEqual(len(essence_set), 5)
        
        # Test set values
        expected_set = set(set_data)
        self.assertEqual(essence_set.values, expected_set)
        
        # Test string representation
        str_repr = str(essence_set)
        self.assertTrue(isinstance(str_repr, str))
        self.assertEqual(str_repr, str(expected_set))
        
        # Test iteration
        elements = []
        for element in essence_set:
            elements.append(element)
        self.assertEqual(sorted(elements), sorted(set_data))
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(essence_set), int))
        
        # Test with different types
        bool_set = EssenceSet([True, False], "find S: set of bool")
        self.assertEqual(bool_set.domain_type, bool)
        self.assertEqual(bool_set.values, {True, False})
        self.assertEqual(len(bool_set), 2)

    def test_essence_set_edge_cases(self):
        # Test empty set
        empty_set = EssenceSet([], "find S: set of int(1..10)")
        self.assertEqual(len(empty_set), 0)
        self.assertEqual(empty_set.values, set())
        
        # Test set with a single element
        single_element = EssenceSet([42], "find S: set of int(0..100)")
        self.assertEqual(len(single_element), 1)
        self.assertEqual(single_element.values, {42})

    
    def test_essence_sequence(self):
        # Testing a sequence with integer elements
        seq_data = [9, 10, 11, 12, 13]
        essence_seq = EssenceSequence(seq_data, "sequence(size 5) of int(9..16)")
        
        # Test basic properties
        self.assertEqual(essence_seq.domain_type, int)
        self.assertEqual(len(essence_seq), 5)
        
        # Test sequence values
        self.assertEqual(essence_seq.values, seq_data)
        
        # Test string representation
        str_repr = str(essence_seq)
        self.assertTrue(isinstance(str_repr, str))
        self.assertEqual(str_repr, str(seq_data))
        
        # Test iteration
        elements = []
        for element in essence_seq:
            elements.append(element)
        self.assertEqual(elements, seq_data)
        
        # Test hash implementation
        self.assertTrue(isinstance(hash(essence_seq), int))
        self.assertEqual(hash(essence_seq), hash(tuple(seq_data)))
        
        # Test with different types
        bool_seq = EssenceSequence([True, False, True], "sequence of bool")
        self.assertEqual(bool_seq.domain_type, bool)
        self.assertEqual(bool_seq.values, [True, False, True])
        self.assertEqual(len(bool_seq), 3)
        
        # Test sequence with duplicate values (should preserve duplicates unlike sets)
        duplicated_data = [1, 2, 3, 3, 4, 5]
        duplicate_seq = EssenceSequence(duplicated_data, "sequence of int(1..10)")
        self.assertEqual(len(duplicate_seq), 6)  # Should be 6, not 5 (preserves duplicates)
        self.assertEqual(duplicate_seq.values, duplicated_data)

    def test_essence_sequence_edge_cases(self):
        # Test empty sequence
        empty_seq = EssenceSequence([], "sequence of int(1..10)")
        self.assertEqual(len(empty_seq), 0)
        self.assertEqual(empty_seq.values, [])
        
        # Test sequence with a single element
        single_element = EssenceSequence([42], "sequence of int(0..100)")
        self.assertEqual(len(single_element), 1)
        self.assertEqual(single_element.values, [42])
        
        # Test sequence with string elements
        str_seq = EssenceSequence(["apple", "banana", "cherry"], "sequence of string")
        self.assertEqual(str_seq.domain_type, str)
        self.assertEqual(str_seq.values, ["apple", "banana", "cherry"])
        self.assertEqual(len(str_seq), 3)
        
        # Test iteration restart
        # First iteration
        elements1 = []
        for element in str_seq:
            elements1.append(element)
        self.assertEqual(elements1, ["apple", "banana", "cherry"])
        
        # Second iteration should restart from beginning
        elements2 = []
        for element in str_seq:
            elements2.append(element)
        self.assertEqual(elements2, ["apple", "banana", "cherry"])

        
if __name__ == "__main__":
    unittest.main()

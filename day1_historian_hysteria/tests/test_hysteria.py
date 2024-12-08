# tests/test_hysteria.py

import unittest
from hysteria import parse_input, compute_total_distance

class TestHistorianHysteria(unittest.TestCase):
    def test_parse_input(self):
        input_data = """
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3
        """
        left_expected = [3, 4, 2, 1, 3, 3]
        right_expected = [4, 3, 5, 3, 9, 3]
        left, right = parse_input(input_data)
        self.assertEqual(left, left_expected)
        self.assertEqual(right, right_expected)
    
    def test_compute_total_distance(self):
        left = [3, 4, 2, 1, 3, 3]
        right = [4, 3, 5, 3, 9, 3]
        # Sorted left: [1, 2, 3, 3, 3, 4]
        # Sorted right: [3, 3, 3, 4, 5, 9]
        # Distances: 2,1,0,1,2,5 → Total: 11
        expected_distance = 11
        distance = compute_total_distance(left, right)
        self.assertEqual(distance, expected_distance)
    
    def test_compute_total_distance_unequal_lengths(self):
        left = [1, 2, 3]
        right = [4, 5]
        with self.assertRaises(ValueError):
            compute_total_distance(left, right)
    
    def test_parse_input_invalid_line(self):
        input_data = """
        1 2
        3
        4 5
        """
        with self.assertRaises(ValueError):
            parse_input(input_data)

if __name__ == '__main__':
    unittest.main()

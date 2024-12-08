# tests/test_reports.py

import unittest
from reports import parse_input, is_monotonic, has_valid_differences, is_safe_report, count_safe_reports

class TestRedNosedReports(unittest.TestCase):
    def test_parse_input(self):
        input_data = """
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
        """
        expected_reports = [
            [7, 6, 4, 2, 1],
            [1, 2, 7, 8, 9],
            [9, 7, 6, 2, 1],
            [1, 3, 2, 4, 5],
            [8, 6, 4, 4, 1],
            [1, 3, 6, 7, 9]
        ]
        reports = parse_input(input_data)
        self.assertEqual(reports, expected_reports)

    def test_is_monotonic_increasing(self):
        report = [1, 2, 3, 4, 5]
        self.assertTrue(is_monotonic(report))

    def test_is_monotonic_decreasing(self):
        report = [5, 4, 3, 2, 1]
        self.assertTrue(is_monotonic(report))

    def test_is_monotonic_not_monotonic(self):
        report = [1, 3, 2, 4, 5]
        self.assertFalse(is_monotonic(report))

    def test_has_valid_differences_valid(self):
        report = [7, 6, 4, 2, 1]
        self.assertTrue(has_valid_differences(report))

    def test_has_valid_differences_invalid_difference(self):
        report = [1, 2, 7, 8, 9]
        self.assertFalse(has_valid_differences(report))

    def test_has_valid_differences_zero_difference(self):
        report = [8, 6, 4, 4, 1]
        self.assertFalse(has_valid_differences(report))

    def test_is_safe_report_safe_decreasing(self):
        report = [7, 6, 4, 2, 1]
        self.assertTrue(is_safe_report(report))

    def test_is_safe_report_safe_increasing(self):
        report = [1, 3, 6, 7, 9]
        self.assertTrue(is_safe_report(report))

    def test_is_safe_report_unsafe_monotonicity(self):
        report = [1, 3, 2, 4, 5]
        self.assertFalse(is_safe_report(report))

    def test_is_safe_report_unsafe_differences(self):
        report = [9, 7, 6, 2, 1]
        self.assertFalse(is_safe_report(report))

    def test_is_safe_report_unsafe_zero_difference(self):
        report = [8, 6, 4, 4, 1]
        self.assertFalse(is_safe_report(report))

    def test_count_safe_reports(self):
        reports = [
            [7, 6, 4, 2, 1],   # Safe
            [1, 2, 7, 8, 9],   # Unsafe
            [9, 7, 6, 2, 1],   # Unsafe
            [1, 3, 2, 4, 5],   # Unsafe
            [8, 6, 4, 4, 1],   # Unsafe
            [1, 3, 6, 7, 9]    # Safe
        ]
        self.assertEqual(count_safe_reports(reports), 2)

    def test_count_safe_reports_all_safe(self):
        reports = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 6, 5]
        ]
        self.assertEqual(count_safe_reports(reports), 3)

    def test_count_safe_reports_none_safe(self):
        reports = [
            [1, 3, 2],
            [4, 4, 5],
            [6, 5, 7]
        ]
        self.assertEqual(count_safe_reports(reports), 0)

    def test_parse_input_with_empty_lines(self):
        input_data = """
        7 6 4 2 1

        1 2 7 8 9

        9 7 6 2 1

        """
        expected_reports = [
            [7, 6, 4, 2, 1],
            [1, 2, 7, 8, 9],
            [9, 7, 6, 2, 1]
        ]
        reports = parse_input(input_data)
        self.assertEqual(reports, expected_reports)

    def test_parse_input_invalid_line(self):
        input_data = """
        7 6 4 2 1
        1 2 7 8
        9 7 6 2 1 0
        """
        expected_reports = [
            [7, 6, 4, 2, 1],
            [1, 2, 7, 8],
            [9, 7, 6, 2, 1, 0]
        ]
        reports = parse_input(input_data)
        self.assertEqual(reports, expected_reports)

if __name__ == '__main__':
    unittest.main()

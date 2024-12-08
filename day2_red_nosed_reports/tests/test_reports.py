# tests/test_reports.py

import unittest
from reports import (
    parse_input,
    is_monotonic,
    has_valid_differences,
    is_safe_report,
    count_safe_reports,
    is_safe_report_with_dampener,
    count_safe_reports_with_dampener
)

class TestRedNosedReports(unittest.TestCase):
    # Existing Part One Tests
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

    # New Part Two Tests
    def test_is_safe_report_with_dampener_already_safe(self):
        report = [7, 6, 4, 2, 1]
        self.assertTrue(is_safe_report_with_dampener(report))

    def test_is_safe_report_with_dampener_needs_removal(self):
        report = [1, 3, 2, 4, 5]
        self.assertTrue(is_safe_report_with_dampener(report))  # Remove 3 to make [1,2,4,5] which is increasing

    def test_is_safe_report_with_dampener_remove_to_safe(self):
        report = [8, 6, 4, 4, 1]
        self.assertTrue(is_safe_report_with_dampener(report))  # Remove one of the 4s to make [8,6,4,1] decreasing

    def test_is_safe_report_with_dampener_cannot_be_made_safe(self):
        report = [1, 2, 7, 8, 9]
        self.assertFalse(is_safe_report_with_dampener(report))  # Cannot make it safe by removing one level

    def test_is_safe_report_with_dampener_multiple_possible_removals(self):
        report = [5, 3, 4, 2, 1]
        # Removing 3: [5,4,2,1] decreasing
        # Removing 4: [5,3,2,1] decreasing
        self.assertTrue(is_safe_report_with_dampener(report))

    def test_is_safe_report_with_dampener_single_level_report(self):
        report = [1]
        self.assertFalse(is_safe_report_with_dampener(report))  # Cannot evaluate safety with less than two levels

    def test_is_safe_report_with_dampener_two_level_report_safe(self):
        report = [1, 2]
        self.assertTrue(is_safe_report_with_dampener(report))  # Already safe

    def test_is_safe_report_with_dampener_two_level_report_unsafe_but_can_be_safe(self):
        report = [1, 1]
        # Remove one level to have [1], but a single level cannot be evaluated as safe
        self.assertFalse(is_safe_report_with_dampener(report))

    def test_count_safe_reports_with_dampener(self):
        reports = [
            [7, 6, 4, 2, 1],   # Safe
            [1, 2, 7, 8, 9],   # Unsafe
            [9, 7, 6, 2, 1],   # Unsafe
            [1, 3, 2, 4, 5],   # Safe by removing 3
            [8, 6, 4, 4, 1],   # Safe by removing one 4
            [1, 3, 6, 7, 9]    # Safe
        ]
        self.assertEqual(count_safe_reports_with_dampener(reports), 4)

    def test_count_safe_reports_with_dampener_all_safe(self):
        reports = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 6, 5]
        ]
        self.assertEqual(count_safe_reports_with_dampener(reports), 3)

    def test_count_safe_reports_with_dampener_none_safe(self):
        reports = [
            [1, 3, 2],
            [4, 4, 5],
            [6, 5, 7]
        ]
        self.assertEqual(count_safe_reports_with_dampener(reports), 0)

    def test_count_safe_reports_with_dampener_mixed(self):
        reports = [
            [7, 6, 4, 2, 1],   # Safe
            [1, 2, 7, 8, 9],   # Unsafe
            [9, 7, 6, 2, 1],   # Unsafe
            [1, 3, 2, 4, 5],   # Safe by removing 3
            [8, 6, 4, 4, 1],   # Safe by removing one 4
            [1, 3, 6, 7, 9],   # Safe
            [5, 3, 4, 2, 1],   # Safe by removing 3 or 4
            [1, 1],            # Unsafe
            [1, 2, 1],         # Safe by removing 2
            [2, 2, 2]          # Unsafe
        ]
        self.assertEqual(count_safe_reports_with_dampener(reports), 6)

if __name__ == '__main__':
    unittest.main()
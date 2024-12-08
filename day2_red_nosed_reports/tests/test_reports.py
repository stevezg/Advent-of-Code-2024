# day2_red_nosed_reports/tests/test_reports.py

import pytest
from day2_red_nosed_reports.reports import (
    parse_input,
    is_monotonic,
    has_valid_differences,
    is_safe_report,
    count_safe_reports,
    is_safe_report_with_dampener,
    count_safe_reports_with_dampener
)

# Fixtures for common input data
@pytest.fixture
def example_reports_part1():
    return [
        [7, 6, 4, 2, 1],   # Safe
        [1, 2, 7, 8, 9],   # Unsafe
        [9, 7, 6, 2, 1],   # Unsafe
        [1, 3, 2, 4, 5],   # Unsafe
        [8, 6, 4, 4, 1],   # Unsafe
        [1, 3, 6, 7, 9]    # Safe
    ]

@pytest.fixture
def example_reports_part2():
    return [
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

# Tests for parse_input
def test_parse_input():
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
    assert reports == expected_reports, "Parsed reports do not match expected output."

def test_parse_input_with_empty_lines():
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
    assert reports == expected_reports, "Parsed reports with empty lines do not match expected output."

def test_parse_input_invalid_line():
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
    assert reports == expected_reports, "Parsed reports with invalid lines do not match expected output."

# Tests for is_monotonic
@pytest.mark.parametrize("report,expected", [
    ([1, 2, 3, 4, 5], True),    # Increasing
    ([5, 4, 3, 2, 1], True),    # Decreasing
    ([1, 3, 2, 4, 5], False),   # Not monotonic
    ([2, 2, 2], False),          # Not strictly monotonic
    ([1, 2, 2, 3], False),       # Not strictly increasing
    ([3, 2, 2, 1], False)        # Not strictly decreasing
])
def test_is_monotonic(report, expected):
    assert is_monotonic(report) == expected, f"Monotonicity test failed for report: {report}"

# Tests for has_valid_differences
@pytest.mark.parametrize("report,expected", [
    ([7, 6, 4, 2, 1], True),    # Differences: -1, -2, -2, -1
    ([1, 2, 7, 8, 9], False),   # Differences: +1, +5, +1, +1
    ([9, 7, 6, 2, 1], False),   # Differences: -2, -1, -4, -1
    ([1, 3, 2, 4, 5], True),    # Differences: +2, -1, +2, +1
    ([8, 6, 4, 4, 1], False),   # Differences: -2, -2, 0, -3
    ([1, 3, 6, 7, 9], True),    # Differences: +2, +3, +1, +2
    ([5, 3, 4, 2, 1], True),    # Differences: -2, +1, -2, -1
    ([1, 1], False),             # Differences: 0
    ([1, 4], True),              # Difference: +3 (valid)
    ([1, 5], False),             # Difference: +4 (invalid)
    ([1, 2], True),              # Difference: +1
    ([2, 1], True),              # Difference: -1
])
def test_has_valid_differences(report, expected):
    assert has_valid_differences(report) == expected, f"Valid differences test failed for report: {report}"

# Tests for is_safe_report
@pytest.mark.parametrize("report,expected", [
    ([7, 6, 4, 2, 1], True),    # Safe: decreasing with valid differences
    ([1, 2, 7, 8, 9], False),   # Unsafe: difference of 5
    ([9, 7, 6, 2, 1], False),   # Unsafe: difference of 4
    ([1, 3, 2, 4, 5], False),   # Unsafe: not monotonic, but has valid differences
    ([8, 6, 4, 4, 1], False),   # Unsafe: zero difference
    ([1, 3, 6, 7, 9], True),    # Safe: increasing with valid differences
    ([2], False),                # Unsafe: single level
    ([1, 1], False),             # Unsafe: zero difference
    ([1, 4], True),              # Safe: difference of 3
    ([1, 5], False),             # Unsafe: difference of 4
    ([1, 2], True),              # Safe: difference of 1
    ([2, 1], True),              # Safe: difference of -1
    ([1, 3, 6], True),           # Safe: increasing with differences 2 and 3
])
def test_is_safe_report(report, expected):
    assert is_safe_report(report) == expected, f"Safe report test failed for report: {report}"

# Tests for count_safe_reports
def test_count_safe_reports(example_reports_part1):
    expected_count = 2
    assert count_safe_reports(example_reports_part1) == expected_count, "Count of safe reports is incorrect."

def test_count_safe_reports_all_safe():
    reports = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 6, 5]
    ]
    expected_count = 3
    assert count_safe_reports(reports) == expected_count, "Count of all safe reports is incorrect."

def test_count_safe_reports_none_safe():
    reports = [
        [1, 3, 2],
        [4, 4, 5],
        [6, 5, 7]
    ]
    expected_count = 0
    assert count_safe_reports(reports) == expected_count, "Count of none safe reports should be 0."

# Tests for is_safe_report_with_dampener
@pytest.mark.parametrize("report,expected", [
    ([7, 6, 4, 2, 1], True),    # Already safe
    ([1, 2, 7, 8, 9], False),   # Cannot be made safe by removing one level
    ([9, 7, 6, 2, 1], False),   # Cannot be made safe by removing one level
    ([1, 3, 2, 4, 5], True),    # Safe by removing 3
    ([8, 6, 4, 4, 1], True),    # Safe by removing one 4
    ([1, 3, 6, 7, 9], True),    # Already safe
    ([5, 3, 4, 2, 1], True),    # Safe by removing 3 or 4
    ([1, 1], False),             # Cannot be made safe (removing one leaves single level)
    ([1, 2, 1], True),           # Safe by removing either 1 to get [2,1] or [1,2]
    ([2, 2, 2], False),          # Cannot be made safe
    ([1, 5, 9], False),          # Cannot be made safe by removing any single level
    ([2, 6, 10], False),         # Cannot be made safe by removing any single level
    ([3, 7, 11], False)          # Cannot be made safe by removing any single level
])
def test_is_safe_report_with_dampener(report, expected):
    assert is_safe_report_with_dampener(report) == expected, f"Safe report with dampener test failed for report: {report}"

# Tests for count_safe_reports_with_dampener
@pytest.mark.parametrize("reports,expected", [
    (
        [
            [7, 6, 4, 2, 1],   # Safe
            [1, 2, 7, 8, 9],   # Unsafe
            [9, 7, 6, 2, 1],   # Unsafe
            [1, 3, 2, 4, 5],   # Safe by removing 3
            [8, 6, 4, 4, 1],   # Safe by removing one 4
            [1, 3, 6, 7, 9]    # Safe
        ],
        4
    ),
    (
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 6, 5]
        ],
        3
    ),
    (
        [
            [1, 5, 9],
            [2, 6, 10],
            [3, 7, 11]
        ],
        0
    ),
    (
        [
            [1, 3, 2],
            [4, 4, 5],
            [6, 5, 7]
        ],
        3  # Corrected from 0 to 3
    ),
    (
        [
            [1, 2, 3, 4],
            [4, 3, 2, 1],
            [1, 2, 1, 2],
            [2, 3, 4, 5]
        ],
        3
    )
])
def test_count_safe_reports_with_dampener(reports, expected):
    actual = count_safe_reports_with_dampener(reports)
    assert actual == expected, f"Count of safe reports with dampener is incorrect. Expected {expected}, got {actual}."

def test_is_safe_report_with_dampener_part2_example():
    reports = [
        [7, 6, 4, 2, 1],   # Safe without removing any level.
        [1, 2, 7, 8, 9],   # Unsafe regardless of removal.
        [9, 7, 6, 2, 1],   # Unsafe regardless of removal.
        [1, 3, 2, 4, 5],   # Safe by removing 3.
        [8, 6, 4, 4, 1],   # Safe by removing one 4.
        [1, 3, 6, 7, 9]    # Safe without removing any level.
    ]
    expected_count = 4
    actual = count_safe_reports_with_dampener(reports)
    assert actual == expected_count, "Count of safe reports with dampener for example data is incorrect."
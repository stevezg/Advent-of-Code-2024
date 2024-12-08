# reports.py

from typing import List
import sys

def parse_input(input_data: str) -> List[List[int]]:
    reports = []
    lines = input_data.strip().splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            levels = list(map(int, line.strip().split()))
            if len(levels) < 2:
                print(f"Warning: Line {line_number} has less than two numbers. Skipping.")
                continue
            reports.append(levels)
        except ValueError as ve:
            print(f"Error parsing line {line_number}: '{line}'. {ve}")
            continue
    return reports

def is_monotonic(report: List[int]) -> bool:
    if len(report) < 2:
        return False
    increasing = all(x < y for x, y in zip(report, report[1:]))
    decreasing = all(x > y for x, y in zip(report, report[1:]))
    return increasing or decreasing

def has_valid_differences(report: List[int]) -> bool:
    for i in range(len(report) - 1):
        diff = abs(report[i+1] - report[i])
        if diff < 1 or diff > 3:
            return False
    return True

def is_safe_report(report: List[int]) -> bool:
    if len(report) < 2:
        return False  # Cannot evaluate safety with less than two levels
    return is_monotonic(report) and has_valid_differences(report)

def count_safe_reports(reports: List[List[int]]) -> int:
    safe_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_count += 1
    return safe_count

def is_safe_report_with_dampener(report: List[int]) -> bool:
    # First, check if the report is already safe
    if is_safe_report(report):
        return True

    # Attempt to remove each level and check if the report becomes safe
    for i in range(len(report)):
        # Create a new report with the i-th level removed
        modified_report = report[:i] + report[i+1:]
        
        # Check if the modified report has at least two levels
        if len(modified_report) < 2:
            continue  # A report with less than two levels cannot be evaluated for safety

        if is_safe_report(modified_report):
            return True  # Found a removal that makes the report safe

    return False  # No single removal makes the report safe

def count_safe_reports_with_dampener(reports: List[List[int]]) -> int:
    safe_count = 0
    for report in reports:
        if is_safe_report_with_dampener(report):
            safe_count += 1
    return safe_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python reports.py <input_file> [--part2]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    part = sys.argv[2] if len(sys.argv) > 2 else "1"

    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
        
        reports = parse_input(input_data)
        
        if part == "2":
            safe_reports = count_safe_reports_with_dampener(reports)
            print(f"Number of Safe Reports (Part 2): {safe_reports}")
        else:
            safe_reports = count_safe_reports(reports)
            print(f"Number of Safe Reports (Part 1): {safe_reports}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# reports.py

from typing import List
import sys

def parse_input(input_data: str) -> List[List[int]]:
    """
    Parses the input data into a list of reports, each report is a list of integers.
    
    Args:
        input_data (str): Multiline string where each line contains numbers separated by spaces.
    
    Returns:
        List[List[int]]: A list of reports with each report represented as a list of integers.
    """
    reports = []
    lines = input_data.strip().splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            # Skip empty lines
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
    """
    Checks if a report is strictly increasing or strictly decreasing.
    
    Args:
        report (List[int]): A list of integers representing a report.
    
    Returns:
        bool: True if the report is monotonic, False otherwise.
    """
    increasing = all(x < y for x, y in zip(report, report[1:]))
    decreasing = all(x > y for x, y in zip(report, report[1:]))
    return increasing or decreasing

def has_valid_differences(report: List[int]) -> bool:
    """
    Checks if all adjacent differences in the report are between 1 and 3 inclusive.
    
    Args:
        report (List[int]): A list of integers representing a report.
    
    Returns:
        bool: True if all adjacent differences are within [1,3], False otherwise.
    """
    for i in range(len(report) - 1):
        diff = abs(report[i+1] - report[i])
        if diff < 1 or diff > 3:
            return False
    return True

def is_safe_report(report: List[int]) -> bool:
    """
    Determines if a report is safe based on monotonicity and adjacency differences.
    
    Args:
        report (List[int]): A list of integers representing a report.
    
    Returns:
        bool: True if the report is safe, False otherwise.
    """
    return is_monotonic(report) and has_valid_differences(report)

def count_safe_reports(reports: List[List[int]]) -> int:
    """
    Counts the number of safe reports in the provided list.
    
    Args:
        reports (List[List[int]]): A list of reports, each report is a list of integers.
    
    Returns:
        int: The total number of safe reports.
    """
    safe_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_count += 1
    return safe_count

def main():
    """
    Main function to read input data from a file and compute the number of safe reports.
    
    Usage:
        python reports.py <input_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python reports.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
        
        reports = parse_input(input_data)
        safe_reports = count_safe_reports(reports)
        print(f"Number of Safe Reports: {safe_reports}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

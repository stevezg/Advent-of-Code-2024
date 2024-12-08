
# day5_print_queue/print_queue.py

import sys
from collections import defaultdict

def parse_input(input_file):
    """
    Parses the input file into rules and updates.

    Args:
        input_file (str): Path to the input file.

    Returns:
        Tuple[List[Tuple[int, int]], List[List[int]]]: A tuple containing:
            - A list of precedence rules as (X, Y) tuples.
            - A list of updates, where each update is a list of page numbers.
    """
    with open(input_file, 'r') as file:
        content = file.read().strip()

    rules_section, updates_section = content.split("\n\n")
    rules = [tuple(map(int, line.split('|'))) for line in rules_section.splitlines()]
    updates = [list(map(int, line.split(','))) for line in updates_section.splitlines()]

    return rules, updates

def is_update_valid(update, rules):
    """
    Checks if an update is valid according to the precedence rules.

    Args:
        update (List[int]): The list of page numbers in the update.
        rules (List[Tuple[int, int]]): A list of precedence rules as (X, Y) tuples.

    Returns:
        bool: True if the update is valid, False otherwise.
    """
    # Build a map of page positions in the update for quick lookup
    page_positions = {page: idx for idx, page in enumerate(update)}

    for x, y in rules:
        # Only check rules where both pages are in the update
        if x in page_positions and y in page_positions:
            if page_positions[x] >= page_positions[y]:
                return False

    return True

def find_middle_page(update):
    """
    Finds the middle page number in the update.

    Args:
        update (List[int]): The list of page numbers in the update.

    Returns:
        int: The middle page number.
    """
    return update[len(update) // 2]

def process_print_queue(input_file):
    """
    Processes the print queue to find the sum of the middle page numbers for valid updates.

    Args:
        input_file (str): Path to the input file.

    Returns:
        int: The sum of the middle page numbers for valid updates.
    """
    rules, updates = parse_input(input_file)
    valid_updates = []

    for update in updates:
        if is_update_valid(update, rules):
            valid_updates.append(update)

    # Calculate the sum of middle page numbers for valid updates
    middle_sum = sum(find_middle_page(update) for update in valid_updates)

    return middle_sum

def main():
    """
    Main function to read input and print the result.

    Usage:
        python print_queue.py <input_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python print_queue.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        result = process_print_queue(input_file)
        print(f"Sum of middle page numbers for valid updates: {result}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
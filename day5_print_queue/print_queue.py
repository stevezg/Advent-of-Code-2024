# day5_print_queue/print_queue.py

import sys
from collections import defaultdict, deque

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

def reorder_update(update, rules):
    """
    Reorders an update according to the precedence rules.

    Args:
        update (List[int]): The list of page numbers in the update.
        rules (List[Tuple[int, int]]): A list of precedence rules as (X, Y) tuples.

    Returns:
        List[int]: The reordered update.
    """
    # Create a graph of dependencies
    graph = defaultdict(list)
    indegree = defaultdict(int)

    for x, y in rules:
        if x in update and y in update:
            graph[x].append(y)
            indegree[y] += 1

    # Add all pages in the update to the indegree map if they have no dependencies
    for page in update:
        indegree.setdefault(page, 0)

    # Perform a topological sort
    queue = deque([node for node in update if indegree[node] == 0])
    sorted_update = []

    while queue:
        current = queue.popleft()
        sorted_update.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update

def find_middle_page(update):
    """
    Finds the middle page number in the update.

    Args:
        update (List[int]): The list of page numbers in the update.

    Returns:
        int: The middle page number.
    """
    return update[len(update) // 2]

def process_incorrect_updates(input_file):
    """
    Processes the print queue to find the sum of the middle page numbers for reordered incorrect updates.

    Args:
        input_file (str): Path to the input file.

    Returns:
        int: The sum of the middle page numbers for reordered incorrect updates.
    """
    rules, updates = parse_input(input_file)
    incorrect_updates = []

    for update in updates:
        if not is_update_valid(update, rules):
            incorrect_updates.append(update)

    # Reorder each incorrect update and calculate the sum of middle pages
    reordered_middle_sum = sum(
        find_middle_page(reorder_update(update, rules)) for update in incorrect_updates
    )

    return reordered_middle_sum

def main():
    """
    Main function to process the print queue for part 2.

    Usage:
        python print_queue.py <input_file> --part2
    """
    if len(sys.argv) != 3 or sys.argv[2] != "--part2":
        print("Usage: python print_queue.py <input_file> --part2")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        result = process_incorrect_updates(input_file)
        print(f"Sum of middle page numbers for reordered incorrect updates: {result}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
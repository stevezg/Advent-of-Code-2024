# hysteria.py

from typing import List, Tuple
import sys

def parse_input(input_data: str) -> Tuple[List[int], List[int]]:
    """
    Parses the input data into two separate lists of integers.

    Args:
        input_data (str): Multiline string with two numbers per line separated by spaces or tabs.

    Returns:
        Tuple[List[int], List[int]]: Two lists containing integers from the left and right columns.
    """
    left_list = []
    right_list = []
    lines = input_data.strip().splitlines()
    for line in lines:
        # Split by any whitespace
        parts = line.strip().split()
        if len(parts) != 2:
            raise ValueError(f"Invalid line format: '{line}'. Each line must contain exactly two numbers.")
        left, right = map(int, parts)
        left_list.append(left)
        right_list.append(right)
    return left_list, right_list

def compute_total_distance(left: List[int], right: List[int]) -> int:
    """
    Computes the total distance between two lists of integers.

    Args:
        left (List[int]): The left list of integers.
        right (List[int]): The right list of integers.

    Returns:
        int: The sum of absolute differences between paired elements.
    """
    if len(left) != len(right):
        raise ValueError("Both lists must have the same number of elements.")
    
     # Sort both lists
    sorted_left = sorted(left)
    sorted_right = sorted(right)
    
    # Compute the sum of absolute differences
    total_distance = 0
    for l, r in zip(sorted_left, sorted_right):
        distance = abs(l - r)
        total_distance += distance
    return total_distance
    
def main():
    """
    Main function to read input from a file and compute the total distance.
    """
    if len(sys.argv) != 2:
        print("Usage: python hysteria.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
        left, right = parse_input(input_data)
        total_distance = compute_total_distance(left, right)
        print(f"Total Distance: {total_distance}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
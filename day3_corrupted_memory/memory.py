# day3_corrupted_memory/memory.py

import re
import sys

def compute_similarity_sum_part1(corrupted_memory: str) -> int:
    """
    Scans the corrupted memory for valid mul(X,Y) instructions and returns the sum of all multiplications.
    
    Parameters:
    - corrupted_memory (str): The string representing the corrupted memory.
    
    Returns:
    - int: The total sum of all valid multiplications.
    """
    # Define the regex pattern for valid mul(X,Y) instructions
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    
    # Find all matches in the corrupted memory
    matches = re.findall(pattern, corrupted_memory)
    
    total_sum = 0
    for x_str, y_str in matches:
        x = int(x_str)
        y = int(y_str)
        product = x * y
        total_sum += product
        print(f"Found mul({x},{y}) → {x} * {y} = {product}")
    
    return total_sum

def compute_similarity_sum_part2(corrupted_memory: str) -> int:
    """
    Scans the corrupted memory for valid mul(X,Y), do(), and don't() instructions.
    Calculates the sum of all enabled mul(X,Y) multiplications based on the current state.
    
    Parameters:
    - corrupted_memory (str): The string representing the corrupted memory.
    
    Returns:
    - int: The total sum of all enabled multiplications.
    """
    # Define the regex pattern for mul(X,Y), do(), and don't() instructions
    # The pattern uses named groups to identify the type of instruction
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)'
    
    # Find all matches in the corrupted memory in order
    matches = re.finditer(pattern, corrupted_memory)
    
    mul_enabled = True  # Initial state: mul instructions are enabled
    total_sum = 0
    
    for match in matches:
        if match.group(0).startswith('mul'):
            # It's a mul(X,Y) instruction
            x_str, y_str = match.group(1), match.group(2)
            if mul_enabled:
                x = int(x_str)
                y = int(y_str)
                product = x * y
                total_sum += product
                print(f"Enabled mul({x},{y}) → {x} * {y} = {product}")
            else:
                print(f"Disabled mul({match.group(1)},{match.group(2)}) → Ignored")
        elif match.group(0) == 'do()':
            mul_enabled = True
            print("Instruction do() encountered → mul instructions enabled.")
        elif match.group(0) == "don't()":
            mul_enabled = False
            print("Instruction don't() encountered → mul instructions disabled.")
    
    return total_sum

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python memory.py <input_file> [--part2]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    part = sys.argv[2] if len(sys.argv) == 3 else "1"
    
    try:
        with open(input_file, 'r') as f:
            corrupted_memory = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)
    
    if part == "--part2":
        print("Running Part Two: Handling do() and don't() instructions.\n")
        total_similarity_sum = compute_similarity_sum_part2(corrupted_memory)
    else:
        print("Running Part One: Summing all valid mul(X,Y) instructions.\n")
        total_similarity_sum = compute_similarity_sum_part1(corrupted_memory)
    
    print(f"\nTotal Similarity Sum: {total_similarity_sum}")

if __name__ == "__main__":
    main()
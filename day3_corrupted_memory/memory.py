# day3_corrupted_memory/memory.py

import re
import sys

def compute_similarity_sum(corrupted_memory: str) -> int:
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
        # print(f"Found mul({x},{y}) → {x} * {y} = {product}")
    
    return total_sum

def main():
    if len(sys.argv) != 2:
        print("Usage: python memory.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            corrupted_memory = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)
    
    total_similarity_sum = compute_similarity_sum(corrupted_memory)
    print(f"\nTotal Similarity Sum: {total_similarity_sum}")

if __name__ == "__main__":
    main()
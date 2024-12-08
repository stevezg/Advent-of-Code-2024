# day4_ceres_search/ceres_search.py

import sys

def parse_grid(input_file):
    """
    Parses the input file into a 2D grid of characters.

    Args:
        input_file (str): Path to the input file.

    Returns:
        List[List[str]]: 2D grid of characters.
    """
    with open(input_file, 'r') as file:
        grid = [list(line.strip()) for line in file if line.strip()]
    return grid

def is_valid_position(x, y, rows, cols):
    """
    Checks if the position (x, y) is within the grid bounds.

    Args:
        x (int): Row index.
        y (int): Column index.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.

    Returns:
        bool: True if the position is valid, False otherwise.
    """
    return 0 <= x < rows and 0 <= y < cols

def count_word_in_direction(grid, word, start_x, start_y, dir_x, dir_y):
    """
    Counts occurrences of the word starting from (start_x, start_y) in a specific direction.

    Args:
        grid (List[List[str]]): 2D grid of characters.
        word (str): Word to search for.
        start_x (int): Starting row index.
        start_y (int): Starting column index.
        dir_x (int): Row direction (-1, 0, 1).
        dir_y (int): Column direction (-1, 0, 1).

    Returns:
        int: 1 if the word is found, 0 otherwise.
    """
    rows, cols = len(grid), len(grid[0])
    for i in range(len(word)):
        x = start_x + i * dir_x
        y = start_y + i * dir_y
        if not is_valid_position(x, y, rows, cols) or grid[x][y] != word[i]:
            return 0
    return 1

def count_word_occurrences(grid, word):
    """
    Counts all occurrences of the word in the grid in all 8 directions.

    Args:
        grid (List[List[str]]): 2D grid of characters.
        word (str): Word to search for.

    Returns:
        int: Total occurrences of the word in the grid.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [
        (-1, 0), (1, 0),  # Vertical
        (0, -1), (0, 1),  # Horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]
    total_count = 0

    for x in range(rows):
        for y in range(cols):
            for dir_x, dir_y in directions:
                total_count += count_word_in_direction(grid, word, x, y, dir_x, dir_y)
    
    return total_count

def main():
    """
    Main function to count occurrences of the word XMAS in the grid.

    Usage:
        python ceres_search.py <input_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python ceres_search.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        grid = parse_grid(input_file)
        word = "XMAS"
        occurrences = count_word_occurrences(grid, word)
        print(f"Total occurrences of '{word}': {occurrences}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
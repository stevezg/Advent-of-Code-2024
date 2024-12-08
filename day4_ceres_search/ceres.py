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

def count_xmas_patterns_part2(grid):
    """
    Counts all occurrences of the X-MAS pattern in the grid (Part 2).

    The X-MAS pattern is defined as:
        M . S
         . A .
        M . S

    Each MAS can be written forwards (MAS) or backwards (SAM).

    Args:
        grid (List[List[str]]): 2D grid of characters.

    Returns:
        int: Total occurrences of the X-MAS pattern in the grid.
    """
    rows, cols = len(grid), len(grid[0])
    total_count = 0

    # Iterate through the grid, treating each cell as a potential center (A)
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            if grid[x][y] == 'A':  # Center of the X-MAS
                # Define the four diagonal positions
                tl = (x - 1, y - 1)  # Top-Left
                br = (x + 1, y + 1)  # Bottom-Right
                tr = (x - 1, y + 1)  # Top-Right
                bl = (x + 1, y - 1)  # Bottom-Left

                # Diagonal 1: Top-Left to Bottom-Right
                diag1 = False
                if is_valid_position(*tl, rows, cols) and is_valid_position(*br, rows, cols):
                    pair1 = (grid[tl[0]][tl[1]], grid[br[0]][br[1]])
                    if pair1 == ('M', 'S') or pair1 == ('S', 'M'):
                        diag1 = True

                # Diagonal 2: Top-Right to Bottom-Left
                diag2 = False
                if is_valid_position(*tr, rows, cols) and is_valid_position(*bl, rows, cols):
                    pair2 = (grid[tr[0]][tr[1]], grid[bl[0]][bl[1]])
                    if pair2 == ('M', 'S') or pair2 == ('S', 'M'):
                        diag2 = True

                # Increment count if both diagonals are valid
                if diag1 and diag2:
                    total_count += 1

    return total_count

def main():
    """
    Main function to count occurrences of either the word XMAS (Part One) or the X-MAS pattern (Part Two).

    Usage:
        python ceres_search.py <input_file> [--part1|--part2]
    """
    if len(sys.argv) != 3:
        print("Usage: python ceres_search.py <input_file> [--part1|--part2]")
        sys.exit(1)

    input_file = sys.argv[1]
    part = sys.argv[2]

    try:
        grid = parse_grid(input_file)

        if part == "--part1":
            word = "XMAS"
            occurrences = count_word_occurrences(grid, word)
            print(f"Total occurrences of '{word}': {occurrences}")
        elif part == "--part2":
            occurrences = count_xmas_patterns_part2(grid)
            print(f"Total occurrences of X-MAS pattern: {occurrences}")
        else:
            print("Invalid option. Use --part1 or --part2.")
            sys.exit(1)

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
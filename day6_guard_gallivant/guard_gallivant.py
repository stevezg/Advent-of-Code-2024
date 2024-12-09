# day6_guard_gallivant/guard_gallivant.py

def parse_map(input_file):
    """
    Parses the input file into a grid and extracts the initial position and direction of the guard.

    Args:
        input_file (str): Path to the input file.

    Returns:
        Tuple[List[List[str]], Tuple[int, int, str]]: The grid and the initial position and direction of the guard.
    """
    grid = []
    guard_position = None
    direction = None

    direction_map = {'^': 'U', '>': 'R', 'v': 'D', '<': 'L'}

    with open(input_file, 'r') as file:
        for row_idx, line in enumerate(file):
            row = list(line.strip())
            for col_idx, char in enumerate(row):
                if char in direction_map:
                    guard_position = (row_idx, col_idx)
                    direction = direction_map[char]
                    row[col_idx] = '.'  # Replace the guard's initial position with empty space
            grid.append(row)

    return grid, guard_position, direction

def move_guard(grid, position, direction):
    """
    Moves the guard according to the patrol rules.

    Args:
        grid (List[List[str]]): The grid representing the map.
        position (Tuple[int, int]): Current position of the guard (row, col).
        direction (str): Current direction ('U', 'R', 'D', 'L').

    Returns:
        Tuple[Tuple[int, int], str]: The new position and direction of the guard.
    """
    rows, cols = len(grid), len(grid[0])
    direction_map = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
    right_turn = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}

    # Get the position in front of the guard
    dr, dc = direction_map[direction]
    next_row, next_col = position[0] + dr, position[1] + dc

    # Check if the guard should turn or move forward
    if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '#':
        # Move forward
        return (next_row, next_col), direction
    else:
        # Turn right
        return position, right_turn[direction]

def simulate_guard(grid, initial_position, initial_direction):
    """
    Simulates the guard's patrol and tracks visited positions.

    Args:
        grid (List[List[str]]): The grid representing the map.
        initial_position (Tuple[int, int]): The initial position of the guard (row, col).
        initial_direction (str): The initial direction of the guard ('U', 'R', 'D', 'L').

    Returns:
        int: The number of distinct positions visited by the guard.
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    position = initial_position
    direction = initial_direction

    while 0 <= position[0] < rows and 0 <= position[1] < cols:
        visited.add(position)
        position, direction = move_guard(grid, position, direction)

    return len(visited)

def main():
    """
    Main function to predict the guard's patrol path.

    Usage:
        python guard_gallivant.py <input_file>
    """
    import sys
    if len(sys.argv) != 2:
        print("Usage: python guard_gallivant.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        grid, initial_position, initial_direction = parse_map(input_file)
        result = simulate_guard(grid, initial_position, initial_direction)
        print(f"Number of distinct positions visited: {result}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
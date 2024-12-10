# guard_gallivant.py

import sys

def parse_map(input_file):
    """
    Parses the input file into a grid and extracts the initial position and direction of the guard.

    Args:
        input_file (str): Path to the input file.

    Returns:
        Tuple[List[List[bool]], Tuple[int, int], int]: 
            - Grid as a 2D list where True represents an obstacle.
            - Initial position as (row, col).
            - Initial direction as an integer (0=Up, 1=Right, 2=Down, 3=Left).
    """
    grid = []
    guard_position = None
    direction = None

    # Map symbols to direction integers
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}

    with open(input_file, 'r') as file:
        for row_idx, line in enumerate(file):
            line = line.rstrip('\n')  # Remove trailing newline
            row = []
            for col_idx, char in enumerate(line):
                if char in direction_map:
                    guard_position = (row_idx, col_idx)
                    direction = direction_map[char]
                    row.append(False)  # Replace guard's position with empty space
                elif char == '#':
                    row.append(True)   # Obstacle
                else:
                    row.append(False)  # Empty space
            grid.append(row)

    if guard_position is None or direction is None:
        raise ValueError("Guard's initial position and direction not found in the map.")

    return grid, guard_position, direction

def simulate_guard(grid, initial_position, initial_direction):
    """
    Simulates the guard's patrol and tracks visited positions.

    Args:
        grid (List[List[bool]]): The grid representing the map.
        initial_position (Tuple[int, int]): The initial position of the guard (row, col).
        initial_direction (int): The initial direction of the guard (0=Up, 1=Right, 2=Down, 3=Left).

    Returns:
        int: The number of distinct positions visited by the guard.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Initialize visited grid
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Direction deltas: Up, Right, Down, Left
    delta_rows = [-1, 0, 1, 0]
    delta_cols = [0, 1, 0, -1]

    # Right turn mapping: 0->1, 1->2, 2->3, 3->0
    right_turn = [1, 2, 3, 0]

    current_row, current_col = initial_position
    current_dir = initial_direction

    # Mark the initial position as visited
    visited[current_row][current_col] = True
    visited_count = 1

    while True:
        # Calculate the next position based on the current direction
        next_row = current_row + delta_rows[current_dir]
        next_col = current_col + delta_cols[current_dir]

        # Check if the next position is within bounds
        if 0 <= next_row < rows and 0 <= next_col < cols:
            if not grid[next_row][next_col]:
                # Move forward
                current_row, current_col = next_row, next_col
                if not visited[current_row][current_col]:
                    visited[current_row][current_col] = True
                    visited_count += 1
                continue  # Proceed to next iteration
            else:
                # Turn right and attempt to move forward in the new direction
                current_dir = right_turn[current_dir]
                # Calculate new next position after turning right
                new_next_row = current_row + delta_rows[current_dir]
                new_next_col = current_col + delta_cols[current_dir]
                if 0 <= new_next_row < rows and 0 <= new_next_col < cols and not grid[new_next_row][new_next_col]:
                    # Move forward in the new direction
                    current_row, current_col = new_next_row, new_next_col
                    if not visited[current_row][current_col]:
                        visited[current_row][current_col] = True
                        visited_count += 1
                    continue  # Proceed to next iteration
                else:
                    # Obstacle after turning right, continue to turn right in the next iteration
                    continue
        else:
            # Guard has moved out of the grid
            break

    return visited_count

def simulate_guard_with_obstacle(grid, initial_position, initial_direction, obstacle_pos):
    """
    Simulate the guard's movement with one additional obstacle placed at obstacle_pos.
    Return True if the guard gets stuck in a loop, False otherwise.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Direction vectors: Up, Right, Down, Left
    delta_rows = [-1, 0, 1, 0]
    delta_cols = [0, 1, 0, -1]

    # Right turn mapping
    right_turn = [1, 2, 3, 0]

    # Place the new obstacle
    (obs_r, obs_c) = obstacle_pos
    grid[obs_r][obs_c] = True

    current_row, current_col = initial_position
    current_dir = initial_direction

    visited_states = set()
    visited_states.add((current_row, current_col, current_dir))

    while True:
        # Compute next forward position
        next_row = current_row + delta_rows[current_dir]
        next_col = current_col + delta_cols[current_dir]

        if 0 <= next_row < rows and 0 <= next_col < cols:
            # If front cell is blocked, turn right
            if grid[next_row][next_col]:
                current_dir = right_turn[current_dir]
                # After turning right, try moving forward again
                next_row = current_row + delta_rows[current_dir]
                next_col = current_col + delta_cols[current_dir]
                
                if 0 <= next_row < rows and 0 <= next_col < cols and not grid[next_row][next_col]:
                    current_row, current_col = next_row, next_col
                else:
                    # If still blocked after turning right, continue turning in next iteration
                    # Just rotate direction again next loop iteration
                    continue
            else:
                # Move forward
                current_row, current_col = next_row, next_col
        else:
            # Guard leaves the map
            grid[obs_r][obs_c] = False  # Remove obstacle
            return False

        # Check for loop
        state = (current_row, current_col, current_dir)
        if state in visited_states:
            # Loop detected
            grid[obs_r][obs_c] = False  # Remove obstacle
            return True
        else:
            visited_states.add(state)


def find_loop_positions(grid, initial_position, initial_direction):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    loop_count = 0

    start_r, start_c = initial_position

    for r in range(rows):
        for c in range(cols):
            # Check only empty cells and not the guard's start
            if (r, c) != (start_r, start_c) and not grid[r][c]:
                if simulate_guard_with_obstacle(grid, initial_position, initial_direction, (r, c)):
                    loop_count += 1

    return loop_count


def main():
    if len(sys.argv) != 2:
        print("Usage: python guard_gallivant.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        grid, initial_position, initial_direction = parse_map(input_file)

        # Part One result
        result_part_one = simulate_guard(grid, initial_position, initial_direction)
        print(f"Number of distinct positions visited (Part One): {result_part_one}")

        # Part Two result
        loop_positions_count = find_loop_positions(grid, initial_position, initial_direction)
        print(f"Number of positions that would create a loop (Part Two): {loop_positions_count}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

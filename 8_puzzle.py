from Simple_8_puzzle import print_puzzle, a_star, manhattan_distance, misplaced_tiles, print_message, is_solvable


def print_moves(heuristic, path, start_state, moves, expanded):
    """
    This code defines a function named print_moves that takes in several parameters and
    prints the puzzle states and messages related to solving the puzzle.

    Args:
    - heuristic (str): The name of the heuristic used to solve the puzzle.
    - path (list): A list of puzzle states representing the path to the goal state.
    - start_state (list): A 2D list representing the initial puzzle state.
    - moves (int): The number of moves required to solve the puzzle.
    - expanded (int): The number of nodes expanded during the puzzle-solving process.
    """
    print("Initial State:")
    print_puzzle(start_state)

    print("Moves to solve:")
    print_puzzle(start_state)

    last_move_num = None  # Variable to store the last move number

    for move_num, state in enumerate(path):
        if move_num == 0:
            # Skip printing Move 0
            continue

        print(f"Move {move_num - 1}")
        print_puzzle(state)
        last_move_num = move_num - 1  # Update the last move number

    if last_move_num is not None:
        print(f"Move {moves}")
        print("\nGoal State:")
        print_puzzle(path[-1])  # Print the final state

    print_message(heuristic, moves, expanded)


# Example usage:
start_state = [
    [5, 2, 8],
    [4, 1, 7],
    [0, 3, 6]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

if is_solvable(start_state):
    path_manhattan, moves_manhattan, expanded_manhattan = a_star(start_state, goal_state, manhattan_distance)
    print_moves("Manhattan Distance", path_manhattan, start_state, moves_manhattan, expanded_manhattan)

    path_misplaced, moves_misplaced, expanded_misplaced = a_star(start_state, goal_state, misplaced_tiles)
    print_moves("Misplaced Tiles", path_misplaced, start_state, moves_misplaced, expanded_misplaced)
else:
    print("Puzzle is not solvable.")

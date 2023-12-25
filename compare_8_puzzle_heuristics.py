import math
from random import shuffle
from simple_8_puzzle import is_solvable, a_star, manhattan_distance, misplaced_tiles

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

puzzle = [item for sublist in goal_state for item in sublist]  # [1, 2, 3, 4, 5, 6, 7, 8, 0]


def generate_random_puzzle():
    """
    Generate a random puzzle by shuffling the numbers 1 to 8 and 0.
    
    Returns:
        list: A 2D list representing the shuffled puzzle.
    """
    shuffle(puzzle)
    return [puzzle[i:i + 3] for i in range(0, 9, 3)]


def generate_100_random_instances():
    """
    Generate 100 random instances of the puzzle.

    Returns:
        A list of 100 random instances of the puzzle.
    """
    instances = []
    while len(instances) < 100:
        puzzle_state = generate_random_puzzle()
        if puzzle_state != goal_state and is_solvable(puzzle_state) and puzzle_state not in instances:
            instances.append(puzzle_state)
    return instances


def calculate_effective_branching_factor(expanded_nodes, depth):
    """
    Calculate the effective branching factor.

    Args:
    - expanded_nodes: The total number of nodes expanded during the search.
    - depth: The depth of the solution.

    Returns:
    - The effective branching factor.
    """
    if depth == 0:
        return 0  # Avoid division by zero
    return math.pow(expanded_nodes, 1 / depth)

def print_compare_8_puzzle_heuristics():
    random_instances = generate_100_random_instances()
    print(" d\t\tEBF Misplaced Tiles\t\tEBF Manhattan Distance")
    for idx, instance in enumerate(random_instances, start=1):
        path_manhattan, moves_manhattan, expanded_manhattan = a_star(instance, goal_state, manhattan_distance)
        path_misplaced, moves_misplaced, expanded_misplaced = a_star(instance, goal_state, misplaced_tiles)

        depth_manhattan = moves_manhattan
        depth_misplaced = moves_misplaced

        ebf_manhattan = calculate_effective_branching_factor(expanded_manhattan, depth_manhattan)
        ebf_misplaced = calculate_effective_branching_factor(expanded_misplaced, depth_misplaced)

        # Print the information in the desired format
        print(f"{idx:2}\t\t\t{ebf_misplaced:.4f}\t\t\t\t\t{ebf_manhattan:.4f}")

print_compare_8_puzzle_heuristics()

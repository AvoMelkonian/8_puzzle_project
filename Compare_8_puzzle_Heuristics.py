from random import shuffle
from Simple_8_puzzle import is_solvable, a_star, manhattan_distance, misplaced_tiles, print_message

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]


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


random_instances = generate_100_random_instances()
for idx, instance in enumerate(random_instances, start=1):
    print(f"Instance: {idx}")
    path_manhattan, moves_manhattan, expanded_manhattan = a_star(instance, goal_state, manhattan_distance)
    path_misplaced, moves_misplaced, expanded_misplaced = a_star(instance, goal_state, misplaced_tiles)
    print_message("Manhattan Distance", moves_manhattan, expanded_manhattan)
    print_message("Misplaced Tiles", moves_misplaced, expanded_misplaced)
    print("\n")

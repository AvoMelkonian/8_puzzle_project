from collections import deque
from heapq import heappop, heappush
from typing import List


class PuzzleNode:
    def __init__(self, state=None, parent=None, heuristic=None, cost=0):
        """
        Initialize a PuzzleNode object.

        Args:
        - state: the state of the puzzle
        - parent: the parent node of the current node (default: None)
        - heuristic: the heuristic value of the node (default: None)
        - cost: the cost of reaching the current node (default: 0)
        """
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost
        self.total_cost = self.cost + self.heuristic

    def __lt__(self, other):
        """
        Compare two PuzzleNode objects based on their total cost.

        Args:
        - other: the other PuzzleNode object to compare with

        Returns:
        - True if the total cost of self is less than the total cost of other, False otherwise.
        """
        if self.total_cost == other.total_cost:
            return self.heuristic < other.heuristic
        return self.total_cost < other.total_cost


class FenwickTree:
    """A Fenwick Tree implementation."""

    def __init__(self, size):
        """Initialize the Fenwick Tree.

        Args:
            size (int): The size of the Fenwick Tree.
        """
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, value):
        """Update the Fenwick Tree.

        Args:
            index (int): The index to update.
            value (int): The value to add to the index.
        """
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def query(self, index):
        """Query the Fenwick Tree.

        Args:
            index (int): The index to query.

        Returns:
            int: The sum of values from index 1 to the given index.
        """
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result


def count_inversions(state):
    """
    The count_inversions function calculates the number of inversions in a
    given state by using a Fenwick Tree data structure.

    Args:
    - state (list of lists): The input state represents a puzzle board,
    where each sublist represents a row and each element represents a number in the puzzle.
    The number 0 represents the empty space.

    Returns:
    - inversions (int): The number of inversions in the given state.
    """
    flat_state = [item for sublist in state for item in sublist if item != 0]
    size = max(flat_state)
    fenwick_tree = FenwickTree(size)
    inversions = 0

    for num in reversed(flat_state):
        inversions += fenwick_tree.query(num - 1)
        fenwick_tree.update(num, 1)

    return inversions


def is_solvable(state):
    """
    The is_solvable function determines whether a given puzzle state is solvable by
    counting the number of inversions in the state and checking if it meets certain conditions.

    Args:
    - state (list of lists): The input state represents a puzzle board,
    where each sublist represents a row and each element represents a number in the puzzle.
    The number 0 represents the empty space.

    Returns:
    -  solvable (bool): True if the puzzle state is solvable, False otherwise.
    """
    inversions = count_inversions(state)
    empty_row = sum(1 for row in state if 0 in row)

    if len(state) % 2 == 1:  # Odd-sized puzzle
        return inversions % 2 == 0
    else:  # Even-sized puzzle
        return (inversions + empty_row) % 2 == 1


def manhattan_distance(state, goal):
    """
    The manhattan_distance function calculates the Manhattan distance between a given state and a goal state.

    Args:
    - state: the state of the puzzle
    - goal: the goal state to reach

    Returns:
    -  an integer representing the Manhattan distance between the current state and the goal state.
    """
    distance = 0
    # Flatten the goal state into a 1-dimensional list called goal_flat.
    goal_flat = [item for sublist in goal for item in sublist]

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != 0:
                goal_position = divmod(goal_flat.index(state[i][j]), len(state))
                distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return distance


def misplaced_tiles(state, goal):
    """
    The misplaced_tiles function calculates the number of tiles that
     are in the wrong position between a given state and a goal state.

    Args:
    - state: the state of the puzzle
    - goal: the goal state to reach

    Returns:
    -  The number of tiles that are in the wrong position between the state and goal matrices.
    """
    count = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != goal[i][j]:
                count += 1
    return count


def a_star(start, goal, heuristic_func):
    """
    This code provides an implementation of the A* algorithm to solve a puzzle.
    The a_star function takes a start state, a goal state, and a heuristic function as inputs,
    and returns the optimal path from the start state to the goal state.

    Args:
    - start: the start state of the puzzle
    - goal: the goal state of the puzzle
    - heuristic_func: a function that calculates the heuristic value for a given state and the goal state

    Returns:
    -  The number of tiles that are in the wrong position between the state and goal matrices.
    """
    open_set = []
    heappush(open_set, (heuristic_func(start, goal), PuzzleNode(start, None, heuristic_func(start, goal))))
    closed_set = set()
    expanded_nodes = 0

    while open_set:
        current_node = heappop(open_set)[1]
        expanded_nodes += 1

        if current_node.state == goal:
            path = deque()
            while current_node:
                path.appendleft(current_node.state)
                current_node = current_node.parent
            total_moves = len(path) - 1  # Subtract 1 to get the number of moves excluding the initial state
            return path, total_moves, expanded_nodes

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor_state in get_neighbors(current_node.state):
            if tuple(map(tuple, neighbor_state)) not in closed_set:
                neighbor_node = PuzzleNode(neighbor_state, current_node, heuristic_func(neighbor_state, goal),
                                           current_node.cost + 1)
                heappush(open_set, (neighbor_node.heuristic + neighbor_node.cost, neighbor_node))

    return None, 0, expanded_nodes


def get_neighbors(state: List[List[int]]) -> deque:
    """
    Returns a deque of neighboring states of the given state.
    
    Args:
        state (list): The current state of the puzzle.
        
    Returns:
        deque: A deque of neighboring states.
    """
    neighbors = deque()
    zero_row, zero_col = find_zero_position(state)

    #            right     left    down      up
    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = zero_row + move[0], zero_col + move[1]
        if 0 <= new_row < len(state) and 0 <= new_col < len(state[0]):
            new_state = [row[:] for row in state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = \
                new_state[new_row][new_col], new_state[zero_row][zero_col]
            neighbors.append(new_state)

    return neighbors


def find_zero_position(state):
    """
    Takes a 2D list called state as input and returns the row
    and column indices of the element with value 0 in the list.

    Args:
    - state (2D list): The input list containing elements.

    Returns:
    -  zero_row: The row index of the element with value 0 in the input list.
    -  zero_col: The column index of the element with value 0 in the input list.
    """
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return i, j


def print_puzzle(state):
    """
    The print_puzzle function takes a 2D list representing a
    puzzle state as input and prints it in a readable format.

    Args:
    - state: a 2D list representing the puzzle state. Each element in the list represents a tile in the puzzle,
    with 0 representing the empty space.
    """
    for row in state:
        print(" ".join(str(x) if x != 0 else ' ' for x in row), end="\n")
    print()


def print_message(heuristic: str, moves: int, expanded: int):
    """
    The print_message function is used to print the number of moves and the number of
    expanded nodes to solve a problem using a specific heuristic.

    Args:
    - heuristic (str): The name of the heuristic used to solve the problem.
    - moves (int): The number of moves required to solve the problem.
    - expanded (int): The number of nodes expanded during the problem-solving process.
    """
    print(f"Moves to solve using {heuristic} heuristic: {moves}")
    print(f"Expanded Nodes to solve using {heuristic} heuristic: {expanded}")


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

path_manhattan, moves_manhattan, expanded_manhattan = a_star(start_state, goal_state, manhattan_distance)
path_misplaced, moves_misplaced, expanded_misplaced = a_star(start_state, goal_state, misplaced_tiles)

if is_solvable(start_state):
    print("Initial State:")
    print_puzzle(start_state)

    print("Goal State:")
    print_puzzle(goal_state)

    print_message("Manhattan Distance", moves_manhattan, expanded_manhattan)
    print_message("Misplaced Tiles", moves_misplaced, expanded_misplaced)
else:
    print("Puzzle is not solvable.")

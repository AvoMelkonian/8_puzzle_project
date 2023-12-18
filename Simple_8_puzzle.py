from collections import deque
from queue import PriorityQueue
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
        The misplaced_tiles function calculates the number of tiles that are in the wrong position between a given state and a goal state.
        
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
    open_set = PriorityQueue()
    open_set.put(PuzzleNode(start, None, heuristic_func(start, goal)))
    closed_set = set()
    expanded_nodes = 0

    while not open_set.empty():
        current_node = open_set.get()
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
                open_set.put(neighbor_node)

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
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            neighbors.append(new_state)

    return neighbors

def find_zero_position(state):
    """
        The find_zero_position function takes a 2D list called state as input and returns the row 
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
    for row in state:
        print(" ".join(map(lambda x: str(x) if x != 0 else ' ', row)))
    print()

# Example usage:
start_state = [
    [1, 2, 3],
    [5, 6, 0],
    [7, 8, 4]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

path_manhattan, moves_manhattan, expanded_manhattan = a_star(start_state, goal_state, manhattan_distance)

print("Initial State:")
print_puzzle(start_state)

print("\nGoal State:")
print_puzzle(goal_state)

print("A* path using Manhattan Distance:")
print("Moves to solve: ")
for move_num, state in enumerate(path_manhattan):
    print(f"Move {move_num}")
    print_puzzle(state)
print(f"Moves to solve using Manhattan Distance heuristic: {moves_manhattan}")
print(f"Expanded Nodes to solve using Manhattan Distance heuristic: {expanded_manhattan}")

# A* path using Misplaced Tiles
path_misplaced, moves_misplaced, expanded_misplaced = a_star(start_state, goal_state, misplaced_tiles)
print("\nA* path using Misplaced Tiles:")
for move_num, state in enumerate(path_misplaced):
    print(f"Move {move_num}")
    print_puzzle(state)
print(f"Moves to solve using missing tiles heuristic: {moves_misplaced}")
print(f"Expanded Nodes to solve using missing tiles heuristic: {expanded_misplaced}")

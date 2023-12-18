import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, heuristic=None, cost=0):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.cost = cost

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def manhattan_distance(state, goal):
    distance = 0
    goal_flat = [item for sublist in goal for item in sublist]

    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != 0:
                goal_position = divmod(goal_flat.index(state[i][j]), len(state))
                distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return distance


def misplaced_tiles(state, goal):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != goal[i][j]:
                count += 1
    return count

def a_star(start, goal, heuristic_func):
    open_set = [PuzzleNode(start, None, heuristic_func(start, goal))]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.state == goal:
            path = []
            while current_node:
                path.insert(0, current_node.state)
                current_node = current_node.parent
            return path

        closed_set.add(tuple(map(tuple, current_node.state)))  # Fix here

        for neighbor_state in get_neighbors(current_node.state):
            if tuple(map(tuple, neighbor_state)) not in closed_set:  # Fix here
                neighbor_node = PuzzleNode(neighbor_state, current_node, heuristic_func(neighbor_state, goal), current_node.cost + 1)
                heapq.heappush(open_set, neighbor_node)

    return None  # No solution found


def get_neighbors(state):
    neighbors = []
    zero_row, zero_col = find_zero_position(state)

    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = zero_row + move[0], zero_col + move[1]
        if 0 <= new_row < len(state) and 0 <= new_col < len(state[0]):
            new_state = [row[:] for row in state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            neighbors.append(new_state)

    return neighbors

def find_zero_position(state):
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

path_manhattan = a_star(start_state, goal_state, manhattan_distance)
path_misplaced = a_star(start_state, goal_state, misplaced_tiles)

print("A* path using Manhattan Distance:")
for state in path_manhattan:
    print_puzzle(state)

print("\nA* path using Misplaced Tiles:")
for state in path_misplaced:
    print_puzzle(state)




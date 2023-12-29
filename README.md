# Project Overview

## Introduction
The project focuses on solving puzzles using the A* algorithm with different heuristic functions. The puzzles are represented as 2D matrices, where each element corresponds to a tile in the puzzle, with 0 indicating an empty space.

## Components

### Puzzle Solver
The puzzle solver is implemented using the A* algorithm, a popular search algorithm for finding the optimal path from a start state to a goal state. It incorporates two heuristic functions:

1. **Manhattan Distance**: Calculates the Manhattan distance between the current state and the goal state. It is a measure of the total distance each tile is from its correct position.

2. **Misplaced Tiles**: Counts the number of tiles that are in the wrong position between the current state and the goal state.

### Fenwick Tree
A Fenwick Tree is utilized to efficiently count inversions in the initial state of the puzzle. The count of inversions is crucial for determining the solvability of the puzzle.

## Python Files
### Simple_8_puzzle :
This code implements the 8-puzzle problem with the 2 heuristics and output count of moves from initial state to the goal state and the number of generated nodes.
### 8_puzzle :
This is an enhanced code that shows all moves from initial state to the goal state.
### Compare_8_puzzle_Heuristics :
This code generates 100 random instances of the game and calculates for each heuristic the effective branching factor for each depth and heuristic

## Usage
The project provides a modular structure that allows users to test the A* algorithm with different instances of puzzles. Users can input random instances, and the program will output information such as the optimal path, number of moves, expanded nodes, and effective branching factor for both heuristic functions.

## Conclusion
The project provides a comprehensive solution for solving puzzles using the A* algorithm and offers insights into the efficiency of different heuristic functions. It can be further expanded and customized for specific puzzle types and heuristic strategies.

## People who worked on this project
ghazal_150589 غزل وليد جبري
avo_108634 افو ملكونيان
yaman_155730 يمان شربجي

## ITE_BAI501_S23_HW

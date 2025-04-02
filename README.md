# Search Algorithms Implementation Assignment

## Overview
The goal of this assignment is to implement and analyze various search algorithms for finding the shortest path in an 8×8 maze. You will evaluate different uninformed and informed search strategies based on their efficiency, completeness, and optimality.

## Group Work Instructions
- This assignment should be completed in groups of three students
- Each student must submit an individual self-reflection report detailing their learning experience from this assignment and the python program

## Task 1: Maze Setup
Using an appropriate data structure, set up the 8×8 maze in your programming environment.

### Maze Construction Rules:
- Each node is represented by its (x, y) coordinates, where x is the column and y is the row
  - Example: node 20 has coordinates (2,4)
- Randomly select a starting node from the first two columns (0-15)
- Randomly select a goal node from the last two columns (48-63)
- Randomly select six barrier nodes from the remaining 62 nodes (these act as obstacles that cannot be traversed)

## Task 2: Uninformed Search Algorithms
Implement the following uninformed search algorithms to find the shortest path in the randomly generated maze:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)

### Required Output for Each Algorithm:
1. Visited nodes list
2. Time taken to find the goal (1 unit per node explored)
3. Final path from start to goal

### Search Execution Rules:
- Process neighbors in increasing numerical order (e.g., for node 12, process 4 → 11 → 13 → 20)
- Only horizontal and vertical moves are allowed (diagonal movement is not permitted)
- Nodes marked as barriers cannot be traversed
- Each node exploration takes 1 unit of time
- All edges have a uniform cost of 1

## Task 3: Heuristic Function (Manhattan Distance)
Implement a function to compute the heuristic cost for each node using the Manhattan distance formula:

\[ d(N, G) = |N_x - G_x| + |N_y - G_y| \]

Where:
- d(N, G) = heuristic cost (Manhattan distance) from node N to goal G
- (N_x, N_y) = coordinates of node N
- (G_x, G_y) = coordinates of Goal node

### Example Calculation:
For node 12 (1,4) and goal node 62 (6,7):
```
d(12, 62) = |1 - 6| + |4 - 7| = 5 + 3 = 8
```

## Task 4: Informed Search Algorithms
Using the heuristic function from Task 3, implement:
- Best-First Search (Greedy Search)
- A* (A-Star) Search

### Required Output for Each Algorithm:
1. Visited nodes list
2. Time taken to find the goal
3. Final path from start to goal

## Task 5: Comparative Analysis
Repeat Tasks 2, 3, and 4 for three additional random mazes (total of four maze setups).

### Analysis Requirements:
- Compare the five search algorithms (BFS, DFS, UCS, Best-First, A* Search) across different mazes
- Discuss results in terms of:
  - Completeness
  - Optimality
  - Time complexity
  - Space complexity

## Task 6: Self-Reflection Report
Each student must submit an individual self-reflection report discussing their learning experience.

### Report Components:

#### Personal Contribution
- Specific tasks you worked on within your group
- How your contributions impacted the overall project

#### Learning Outcomes
- New concepts or skills learned through this assignment
- Challenges faced while implementing search algorithms and how you overcame them

#### Comparison of Search Strategies
- Insights gained from implementing different search algorithms
- Key differences observed between uninformed and informed search techniques

#### Future Improvements
- How you would improve your approach if given a similar assignment
- Additional optimizations or algorithms you would consider implementing

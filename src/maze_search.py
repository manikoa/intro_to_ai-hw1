from typing import List, Tuple, Set, Dict
from queue import Queue, PriorityQueue
import time
from dataclasses import dataclass
from enum import Enum
import random

class NodeType(Enum):
    EMPTY = 0
    START = 1
    GOAL = 2
    BARRIER = 3

@dataclass
class Node:
    id: int
    x: int  # column
    y: int  # row
    type: NodeType = NodeType.EMPTY
    
    def __lt__(self, other):
        return self.id < other.id

class Maze:
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.nodes: Dict[int, Node] = {}
        self.start_node: Node = None
        self.goal_node: Node = None
        self.barriers: Set[int] = set()
        
        # Initialize the maze
        self._init_maze()
        
    def _init_maze(self):
        # Create all nodes
        for y in range(self.height):
            for x in range(self.width):
                node_id = y * self.width + x
                self.nodes[node_id] = Node(node_id, x, y)
    
    def setup_maze(self, start_id: int, goal_id: int, barrier_ids: List[int]):
        """Setup maze with given configuration"""
        # Set start node
        self.start_node = self.nodes[start_id]
        self.start_node.type = NodeType.START
        
        # Set goal node
        self.goal_node = self.nodes[goal_id]
        self.goal_node.type = NodeType.GOAL
        
        # Set barriers
        self.barriers = set(barrier_ids)
        for barrier_id in barrier_ids:
            self.nodes[barrier_id].type = NodeType.BARRIER
    
    def get_neighbors(self, node_id: int) -> List[int]:
        """Get valid neighbors of a node in increasing numerical order"""
        node = self.nodes[node_id]
        x, y = node.x, node.y
        
        # Potential neighbors (up, left, right, down)
        neighbors = []
        
        # Up
        if y > 0:
            neighbors.append((y-1) * self.width + x)
        # Left
        if x > 0:
            neighbors.append(y * self.width + (x-1))
        # Right
        if x < self.width - 1:
            neighbors.append(y * self.width + (x+1))
        # Down
        if y < self.height - 1:
            neighbors.append((y+1) * self.width + x)
            
        # Filter out barriers and sort
        return sorted([n for n in neighbors if n not in self.barriers])
    
    def manhattan_distance(self, node_id: int) -> int:
        """Calculate Manhattan distance from node to goal"""
        node = self.nodes[node_id]
        return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y)

class SearchResult:
    def __init__(self):
        self.visited: List[int] = []
        self.path: List[int] = []
        self.time_units: int = 0

class MazeSearch:
    def __init__(self, maze: Maze):
        self.maze = maze
    
    def bfs(self) -> SearchResult:
        """Breadth-First Search implementation"""
        result = SearchResult()
        start_id = self.maze.start_node.id
        goal_id = self.maze.goal_node.id
        
        queue = Queue()
        queue.put(start_id)
        visited = {start_id: None}  # node_id -> parent_id
        
        while not queue.empty():
            current_id = queue.get()
            result.visited.append(current_id)
            result.time_units += 1
            
            if current_id == goal_id:
                break
                
            for neighbor_id in self.maze.get_neighbors(current_id):
                if neighbor_id not in visited:
                    visited[neighbor_id] = current_id
                    queue.put(neighbor_id)
        
        # Reconstruct path if goal was found
        if goal_id in visited:
            current_id = goal_id
            while current_id is not None:
                result.path.insert(0, current_id)
                current_id = visited[current_id]
                
        return result
    
    def dfs(self) -> SearchResult:
        """Depth-First Search implementation"""
        result = SearchResult()
        start_id = self.maze.start_node.id
        goal_id = self.maze.goal_node.id
        
        stack = [start_id]
        visited = {start_id: None}  # node_id -> parent_id
        
        while stack:
            current_id = stack.pop()
            result.visited.append(current_id)
            result.time_units += 1
            
            if current_id == goal_id:
                break
                
            # Process neighbors in reverse order to maintain increasing order when popping
            for neighbor_id in reversed(self.maze.get_neighbors(current_id)):
                if neighbor_id not in visited:
                    visited[neighbor_id] = current_id
                    stack.append(neighbor_id)
        
        # Reconstruct path if goal was found
        if goal_id in visited:
            current_id = goal_id
            while current_id is not None:
                result.path.insert(0, current_id)
                current_id = visited[current_id]
                
        return result
    
    def ucs(self) -> SearchResult:
        """Uniform Cost Search implementation"""
        result = SearchResult()
        start_id = self.maze.start_node.id
        goal_id = self.maze.goal_node.id
        
        frontier = PriorityQueue()
        frontier.put((0, start_id))
        visited = {start_id: None}  # node_id -> parent_id
        cost_so_far = {start_id: 0}
        
        while not frontier.empty():
            current_cost, current_id = frontier.get()
            result.visited.append(current_id)
            result.time_units += 1
            
            if current_id == goal_id:
                break
                
            for neighbor_id in self.maze.get_neighbors(current_id):
                new_cost = cost_so_far[current_id] + 1  # uniform cost of 1
                
                if neighbor_id not in cost_so_far or new_cost < cost_so_far[neighbor_id]:
                    cost_so_far[neighbor_id] = new_cost
                    frontier.put((new_cost, neighbor_id))
                    visited[neighbor_id] = current_id
        
        # Reconstruct path if goal was found
        if goal_id in visited:
            current_id = goal_id
            while current_id is not None:
                result.path.insert(0, current_id)
                current_id = visited[current_id]
                
        return result
    
    def best_first_search(self) -> SearchResult:
        """Best-First Search (Greedy) implementation"""
        result = SearchResult()
        start_id = self.maze.start_node.id
        goal_id = self.maze.goal_node.id
        
        frontier = PriorityQueue()
        frontier.put((self.maze.manhattan_distance(start_id), start_id))
        visited = {start_id: None}  # node_id -> parent_id
        
        while not frontier.empty():
            _, current_id = frontier.get()
            result.visited.append(current_id)
            result.time_units += 1
            
            if current_id == goal_id:
                break
                
            for neighbor_id in self.maze.get_neighbors(current_id):
                if neighbor_id not in visited:
                    visited[neighbor_id] = current_id
                    frontier.put((self.maze.manhattan_distance(neighbor_id), neighbor_id))
        
        # Reconstruct path if goal was found
        if goal_id in visited:
            current_id = goal_id
            while current_id is not None:
                result.path.insert(0, current_id)
                current_id = visited[current_id]
                
        return result
    
    def astar(self) -> SearchResult:
        """A* Search implementation"""
        result = SearchResult()
        start_id = self.maze.start_node.id
        goal_id = self.maze.goal_node.id
        
        frontier = PriorityQueue()
        frontier.put((0, start_id))
        visited = {start_id: None}  # node_id -> parent_id
        cost_so_far = {start_id: 0}
        
        while not frontier.empty():
            _, current_id = frontier.get()
            result.visited.append(current_id)
            result.time_units += 1
            
            if current_id == goal_id:
                break
                
            for neighbor_id in self.maze.get_neighbors(current_id):
                new_cost = cost_so_far[current_id] + 1  # uniform cost of 1
                
                if neighbor_id not in cost_so_far or new_cost < cost_so_far[neighbor_id]:
                    cost_so_far[neighbor_id] = new_cost
                    priority = new_cost + self.maze.manhattan_distance(neighbor_id)
                    frontier.put((priority, neighbor_id))
                    visited[neighbor_id] = current_id
        
        # Reconstruct path if goal was found
        if goal_id in visited:
            current_id = goal_id
            while current_id is not None:
                result.path.insert(0, current_id)
                current_id = visited[current_id]
                
        return result

def main():
    # Create maze with the given configuration
    maze = Maze()
    
    # Setup maze with the configuration from the image
    start_id = 12  # (1,4)
    goal_id = 62   # (6,7)
    barrier_ids = [8, 23, 34, 36, 49, 60]  # Barriers from the image
    
    maze.setup_maze(start_id, goal_id, barrier_ids)
    
    # Create search instance
    search = MazeSearch(maze)
    
    # Run all search algorithms
    algorithms = {
        'BFS': search.bfs,
        'DFS': search.dfs,
        'UCS': search.ucs,
        'Best-First': search.best_first_search,
        'A*': search.astar
    }
    
    print("Maze Search Results:")
    print("-" * 50)
    
    # Import visualization if matplotlib is available
    try:
        from maze_visualizer import visualize_maze_result
        can_visualize = True
    except ImportError:
        can_visualize = False
        print("Warning: matplotlib not available, skipping visualization")
    
    for name, algorithm in algorithms.items():
        result = algorithm()
        print(f"\n{name} Search:")
        print(f"Time units: {result.time_units}")
        print(f"Visited nodes: {result.visited}")
        print(f"Path found: {result.path}")
        print(f"Path length: {len(result.path) - 1}")  # -1 because we don't count the start node as a step
        
        if can_visualize:
            visualize_maze_result(maze, result.visited, result.path, f"{name} Search Results")

if __name__ == "__main__":
    main()
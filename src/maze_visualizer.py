import numpy as np
import matplotlib.pyplot as plt
from maze_search import Maze, NodeType
import os

def visualize_maze_result(maze: Maze, visited: list, path: list, title: str, save: bool = True):
    """Visualize the maze with search results"""
    # Create a grid for visualization
    grid = np.zeros((maze.height, maze.width))
    
    # Mark barriers
    for barrier_id in maze.barriers:
        node = maze.nodes[barrier_id]
        grid[node.y, node.x] = 1
    
    # Create figure and axis
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')
    
    # Plot visited nodes
    visited_x = [maze.nodes[n].x for n in visited]
    visited_y = [maze.nodes[n].y for n in visited]
    plt.plot(visited_x, visited_y, 'b.', alpha=0.3, label='Visited')
    
    # Plot path
    if path:
        path_x = [maze.nodes[n].x for n in path]
        path_y = [maze.nodes[n].y for n in path]
        plt.plot(path_x, path_y, 'g-', linewidth=2, label='Path')
    
    # Mark start and goal
    plt.plot(maze.start_node.x, maze.start_node.y, 'yo', markersize=15, label='Start')
    plt.plot(maze.goal_node.x, maze.goal_node.y, 'ro', markersize=15, label='Goal')
    
    # Customize plot
    plt.grid(True)
    plt.title(title)
    plt.legend()
    
    if save:
        # Create filename from title
        filename = title.lower().replace(' ', '_') + '.png'
        # Ensure data directory exists
        os.makedirs('../data', exist_ok=True)
        # Save plot
        plt.savefig(os.path.join('../data', filename))
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    from maze_search import main
    main()
"""
Visualization of the initial grid environment before running any algorithms.
This shows the grid with coordinates and initial utility values.
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from src.utils.config import NUM_COLS, NUM_ROWS, GREEN_SQUARES, BROWN_SQUARES, WALLS_SQUARES

class InitialGridVisualizer:
    """
    Visualizes the initial grid environment before running any algorithms.
    """
    
    @staticmethod
    def visualize_initial_grid(grid, title="Initial Grid Environment", filename="initial_grid.png"):
        """
        Creates a visualization of the initial grid environment with coordinates and rewards.
        
        Args:
            grid (list): The grid environment
            title (str): Title for the visualization
            filename (str): Filename to save the visualization (without the path)
        """
        # Make sure output directory exists
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create full file path
        filepath = os.path.join(output_dir, filename)
        
        print(f"Creating initial grid visualization: {title}")
        print(f"Saving to: {os.path.abspath(filepath)}")
        
        # Create a figure with a specific size
        plt.figure(figsize=(12, 10))
        
        # Create a grid
        ax = plt.gca()
        
        # Define colors for different cell types
        colors = {
            'white': '#f0f0f0',    # White/default cells
            'green': '#c8e6c9',    # Green cells (positive reward)
            'brown': '#ffccbc',    # Brown cells (negative reward)
            'wall': '#757575',     # Wall cells
            'start': '#e8f5e9'     # Starting position (light green)
        }
        
        # For each cell in the grid
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # Cell boundaries
                rect = plt.Rectangle((col, row), 1, 1, edgecolor='gray', linewidth=1, fill=False)
                ax.add_patch(rect)
                
                # Determine cell color and reward based on type
                if grid[col][row].is_wall:
                    color = colors['wall']
                    reward = 0.0
                elif (col, row) in GREEN_SQUARES:
                    color = colors['green']
                    reward = 1.0
                elif (col, row) in BROWN_SQUARES:
                    color = colors['brown']
                    reward = -1.0
                else:
                    color = colors['white']
                    reward = -0.04
                
                # Fill the cell with color
                rect = plt.Rectangle((col, row), 1, 1, facecolor=color, alpha=0.7)
                ax.add_patch(rect)
                
                # Add cell coordinates and reward
                if grid[col][row].is_wall:
                    plt.text(col + 0.5, row + 0.5, f"({col},{row})\nWALL", 
                             ha='center', va='center', fontweight='bold')
                else:
                    plt.text(col + 0.5, row + 0.5, f"({col},{row})\nr={reward:.2f}\nu=0.00", 
                             ha='center', va='center', fontsize=8)
        
        # Set the limits and aspect ratio
        plt.xlim(0, NUM_COLS)
        plt.ylim(0, NUM_ROWS)
        plt.gca().invert_yaxis()  # Invert y-axis to match grid coordinates
        plt.axis('equal')
        
        # Remove ticks and set grid
        plt.xticks(np.arange(0.5, NUM_COLS, 1), [str(i) for i in range(NUM_COLS)])
        plt.yticks(np.arange(0.5, NUM_ROWS, 1), [str(i) for i in range(NUM_ROWS)])
        plt.grid(False)
        
        # Add title and adjust layout
        plt.title(title)
        plt.tight_layout()
        
        # Create a legend
        green_patch = Rectangle((0, 0), 1, 1, facecolor=colors['green'], alpha=0.7, label='Green (+1.0)')
        brown_patch = Rectangle((0, 0), 1, 1, facecolor=colors['brown'], alpha=0.7, label='Brown (-1.0)')
        white_patch = Rectangle((0, 0), 1, 1, facecolor=colors['white'], alpha=0.7, label='White (-0.04)')
        wall_patch = Rectangle((0, 0), 1, 1, facecolor=colors['wall'], alpha=0.7, label='Wall')
        
        plt.legend(handles=[green_patch, brown_patch, white_patch, wall_patch], 
                  loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4)
        
        try:
            # Save the plot with the provided filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Successfully saved initial grid visualization to {filepath}")
            plt.show()
            return True
        except Exception as e:
            print(f"Error saving initial grid visualization: {e}")
            return False

# Add this function to create initial utilities visualization
def visualize_initial_grid_with_utilities():
    """
    Example usage to visualize the initial grid environment.
    """
    from src.core.grid_environment import GridEnvironment
    
    # Initialize the grid environment
    grid_env = GridEnvironment()
    
    # Visualize the initial grid
    InitialGridVisualizer.visualize_initial_grid(grid_env.get_grid())
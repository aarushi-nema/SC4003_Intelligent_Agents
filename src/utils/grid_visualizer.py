"""
Grid visualization for MDP policy and utility values - CLEAN LAYOUT.
This creates a clean layout with no overlapping elements.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from src.core.actions import Action
from src.utils.config import NUM_COLS, NUM_ROWS, GREEN_SQUARES, BROWN_SQUARES, WALLS_SQUARES

class GridVisualizer:
    """
    Visualizes the grid environment with policy actions and utility values.
    """
    
    @staticmethod
    def visualize_policy_grid(grid, util_arr, title="Optimal Policy and Utilities", filename="policy_visualization.png"):
        """
        Creates a visualization of the grid with policy actions and utility values.
        
        Args:
            grid (list): The grid environment
            util_arr (list): Utility values for all states
            title (str): Title for the visualization
            filename (str): Filename to save the visualization (without the path)
        """
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
            'start': '#e0e0e0'     # Starting position
        }
        
        # Define arrow properties
        arrow_props = dict(
            arrowstyle='->', 
            linewidth=2, 
            color='black'
        )
        
        # For each cell in the grid
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # Cell boundaries
                rect = plt.Rectangle((col, row), 1, 1, edgecolor='gray', linewidth=1, fill=False)
                ax.add_patch(rect)
                
                # Determine cell color based on type
                if grid[col][row].is_wall:
                    color = colors['wall']
                elif (col, row) in GREEN_SQUARES:
                    color = colors['green']
                elif (col, row) in BROWN_SQUARES:
                    color = colors['brown']
                else:
                    color = colors['white']
                
                # Fill the cell with color
                rect = plt.Rectangle((col, row), 1, 1, facecolor=color, alpha=0.7)
                ax.add_patch(rect)
                
                # Skip walls for action and utility
                if grid[col][row].is_wall:
                    plt.text(col + 0.5, row + 0.5, "WALL", ha='center', va='center', fontweight='bold')
                    continue
                
                # Get action and utility
                action = util_arr[col][row].get_action()
                utility = util_arr[col][row].get_util()
                
                # Action text at top
                plt.text(col + 0.5, row + 0.15, f"{action.value if action else 'None'}", 
                         ha='center', va='center', fontsize=9, color='darkgreen', fontweight='bold')
                
                # Utility value at bottom
                plt.text(col + 0.5, row + 0.85, f"{utility:.3f}", ha='center', va='center', fontsize=9)
                
                # Draw arrow in the middle section
                if action == Action.UP:
                    plt.annotate('', xy=(col + 0.5, row + 0.4), xytext=(col + 0.5, row + 0.6), arrowprops=arrow_props)
                elif action == Action.DOWN:
                    plt.annotate('', xy=(col + 0.5, row + 0.6), xytext=(col + 0.5, row + 0.4), arrowprops=arrow_props)
                elif action == Action.LEFT:
                    plt.annotate('', xy=(col + 0.35, row + 0.5), xytext=(col + 0.65, row + 0.5), arrowprops=arrow_props)
                elif action == Action.RIGHT:
                    plt.annotate('', xy=(col + 0.65, row + 0.5), xytext=(col + 0.35, row + 0.5), arrowprops=arrow_props)
        
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
        
        # Save the plot with the provided filename
        plt.savefig(f'output/{filename}', dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def compare_policies(grid, value_policy, policy_policy, title="Policy Comparison", filename="policy_comparison.png"):
        """
        Creates a side-by-side comparison of value iteration and policy iteration results.
        
        Args:
            grid (list): The grid environment
            value_policy (list): Utility values from value iteration
            policy_policy (list): Utility values from policy iteration
            title (str): Title for the visualization
            filename (str): Filename to save the visualization
        """
        # Create a figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
        # Define colors for different cell types
        colors = {
            'white': '#f0f0f0',    # White/default cells
            'green': '#c8e6c9',    # Green cells (positive reward)
            'brown': '#ffccbc',    # Brown cells (negative reward)
            'wall': '#757575',     # Wall cells
            'start': '#e0e0e0'     # Starting position
        }
        
        # Define arrow properties
        arrow_props = dict(
            arrowstyle='->', 
            linewidth=2, 
            color='black'
        )
        
        # Function to draw grid on a specific axis
        def draw_grid(ax, policy_arr, subtitle):
            ax.set_title(subtitle)
            
            # For each cell in the grid
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    # Cell boundaries
                    rect = Rectangle((col, row), 1, 1, edgecolor='gray', linewidth=1, fill=False)
                    ax.add_patch(rect)
                    
                    # Determine cell color based on type
                    if grid[col][row].is_wall:
                        color = colors['wall']
                    elif (col, row) in GREEN_SQUARES:
                        color = colors['green']
                    elif (col, row) in BROWN_SQUARES:
                        color = colors['brown']
                    else:
                        color = colors['white']
                    
                    # Fill the cell with color
                    rect = Rectangle((col, row), 1, 1, facecolor=color, alpha=0.7)
                    ax.add_patch(rect)
                    
                    # Skip walls for action and utility
                    if grid[col][row].is_wall:
                        ax.text(col + 0.5, row + 0.5, "WALL", ha='center', va='center', fontweight='bold')
                        continue
                    
                    # Get action and utility
                    action = policy_arr[col][row].get_action()
                    utility = policy_arr[col][row].get_util()
                    
                    # Action text at top
                    ax.text(col + 0.5, row + 0.15, f"{action.value if action else 'None'}", 
                            ha='center', va='center', fontsize=9, color='darkgreen', fontweight='bold')
                    
                    # Utility value at bottom
                    ax.text(col + 0.5, row + 0.85, f"{utility:.3f}", ha='center', va='center', fontsize=9)
                    
                    # Draw arrow in the middle section
                    if action == Action.UP:
                        ax.annotate('', xy=(col + 0.5, row + 0.4), xytext=(col + 0.5, row + 0.6), arrowprops=arrow_props)
                    elif action == Action.DOWN:
                        ax.annotate('', xy=(col + 0.5, row + 0.6), xytext=(col + 0.5, row + 0.4), arrowprops=arrow_props)
                    elif action == Action.LEFT:
                        ax.annotate('', xy=(col + 0.35, row + 0.5), xytext=(col + 0.65, row + 0.5), arrowprops=arrow_props)
                    elif action == Action.RIGHT:
                        ax.annotate('', xy=(col + 0.65, row + 0.5), xytext=(col + 0.35, row + 0.5), arrowprops=arrow_props)
            
            # Set the limits and aspect ratio
            ax.set_xlim(0, NUM_COLS)
            ax.set_ylim(0, NUM_ROWS)
            ax.invert_yaxis()  # Invert y-axis to match grid coordinates
            ax.set_aspect('equal')
            
            # Remove ticks and set grid
            ax.set_xticks(np.arange(0.5, NUM_COLS, 1))
            ax.set_xticklabels([str(i) for i in range(NUM_COLS)])
            ax.set_yticks(np.arange(0.5, NUM_ROWS, 1))
            ax.set_yticklabels([str(i) for i in range(NUM_ROWS)])
        
        # Draw both grids
        draw_grid(ax1, value_policy, "Value Iteration")
        draw_grid(ax2, policy_policy, "Policy Iteration")
        
        # Add main title
        fig.suptitle(title, fontsize=16)
        
        # Create a legend
        green_patch = Rectangle((0, 0), 1, 1, facecolor=colors['green'], alpha=0.7, label='Green (+1.0)')
        brown_patch = Rectangle((0, 0), 1, 1, facecolor=colors['brown'], alpha=0.7, label='Brown (-1.0)')
        white_patch = Rectangle((0, 0), 1, 1, facecolor=colors['white'], alpha=0.7, label='White (-0.04)')
        wall_patch = Rectangle((0, 0), 1, 1, facecolor=colors['wall'], alpha=0.7, label='Wall')
        
        fig.legend(handles=[green_patch, brown_patch, white_patch, wall_patch], 
                  loc='upper center', bbox_to_anchor=(0.5, 0), ncol=4)
        
        plt.tight_layout()
        fig.subplots_adjust(top=0.85)  # Adjust top spacing for the main title
        
        # Save the comparison visualization
        plt.savefig(f'output/{filename}', dpi=300, bbox_inches='tight')
        plt.show()
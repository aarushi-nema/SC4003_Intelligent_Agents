"""
Display manager for visualization.
"""
from src.utils.config import (
    NUM_COLS, NUM_ROWS, AGENT_START_COL, AGENT_START_ROW,
    WHITE_REWARD, DISCOUNT, EPSILON, K
)

class DisplayManager:
    """
    Manages display of grid environment, utilities, and policies.
    """
    
    @staticmethod
    def display_utilities(grid, util_arr):
        """
        Display the utilities of all the (non-wall) states.
        
        Args:
            grid (list): The grid environment.
            util_arr (list): Utility values for all states.
        """
        sb = DisplayManager.frame_title("Utility Values of States")
        
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                if not grid[col][row].is_wall:
                    util = f"{util_arr[col][row].get_util():.8g}"
                    sb += f"({col}, {row}): {util}\n"
        
        print(sb)
    
    @staticmethod
    def display_iterations_count(num):
        """
        Display the number of iterations.
        
        Args:
            num (int): Number of iterations.
        """
        sb = DisplayManager.frame_title("Total Iteration Count")
        sb += f"Iterations: {num}\n"
        with open(r'C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\algorithm_performance.txt', 'a') as file:
            file.write(sb)
        print(sb)
    
    @staticmethod
    def display_experiment_setup(is_value_iteration, converge_threshold=0.0):
        """
        Display the experiment setup.
        
        Args:
            is_value_iteration (bool): Whether the algorithm is value iteration.
            converge_threshold (float): Convergence threshold for value iteration.
        """
        sb = DisplayManager.frame_title("Experiment Setup")
        
        if is_value_iteration:
            sb += f"Discount Factor\t\t:\t{DISCOUNT}\n"
            sb += f"Utility Upper Bound\t:\t{EPSILON / ((1.0 - DISCOUNT) / DISCOUNT):.5g}\n"
            sb += f"Max Reward(Rmax)\t:\t{1.0}\n"
            sb += f"Constant 'c'\t\t:\t{EPSILON}\n"
            sb += f"Epsilon Value(c * Rmax)\t:\t{EPSILON}\n"
            sb += f"Convergence Threshold\t:\t{converge_threshold:.5f}\n\n"
        else:
            sb += f"Discount\t:\t{DISCOUNT}\n"
            sb += f"k\t\t:\t{K}\n\n"
        
        print(sb)
    
    @staticmethod
    def frame_title(title):
        """
        Create a framed title.
        
        Args:
            title (str): The title to frame.
            
        Returns:
            str: The framed title.
        """
        sb = "\n"
        # sb += "*" * (len(title) + 4) + "\n"
        sb += f"---- {title} -----\n"
        # sb += "*" * (len(title) + 4) + "\n\n"
        return sb
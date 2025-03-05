"""
Display manager for visualization.
"""
from src.utils.constants import (
    NUM_COLS, NUM_ROWS, AGENT_START_COL, AGENT_START_ROW,
    WHITE_REWARD, DISCOUNT, EPSILON, K
)

class DisplayManager:
    """
    Manages display of grid environment, utilities, and policies.
    """
    
    @staticmethod
    def display_grid(grid):
        """
        Display the Grid Environment.
        
        Args:
            grid (list): The grid environment.
        """
        sb = DisplayManager.frame_title("Grid Environment")
        sb += "|"
        for _ in range(NUM_COLS):
            sb += "--------|"
        sb += "\n"
        
        for row in range(NUM_ROWS):
            sb += "|"
            for _ in range(NUM_COLS):
                sb += "        |"
            sb += "\n"
            
            sb += "|"
            for col in range(NUM_COLS):
                state = grid[col][row]
                if col == AGENT_START_COL and row == AGENT_START_ROW:
                    temp = " Start"
                elif state.is_wall:
                    temp = "Wall"
                elif state.get_reward() != WHITE_REWARD:
                    temp = str(state.get_reward())
                    if temp[0] != '-':
                        temp = " " + temp
                else:
                    temp = "    "
                
                n = (8 - len(temp)) // 2
                str_pad = " " * n
                sb += str_pad + temp + str_pad + "|"
            
            sb += "\n|"
            for _ in range(NUM_COLS):
                sb += "        |"
            sb += "\n"
            
            sb += "|"
            for _ in range(NUM_COLS):
                sb += "--------|"
            sb += "\n"
        
        print(sb)
    
    @staticmethod
    def display_policy(util_arr):
        """
        Display the policy (i.e., the action to be taken at each state).
        
        Args:
            util_arr (list): Utility values for all states.
        """
        sb = DisplayManager.frame_title("Plot of Optimal Policy")
        sb += "|"
        for _ in range(NUM_COLS):
            sb += "--------|"
        sb += "\n"
        
        for row in range(NUM_ROWS):
            sb += "|"
            for _ in range(NUM_COLS):
                sb += "        |"
            sb += "\n"
            
            sb += "|"
            for col in range(NUM_COLS):
                util = util_arr[col][row].get_action_str()
                n = (9 - len(util)) // 2
                str_pad = " " * n
                str_pad1 = " " * (n - 1 if n > 0 else 0)
                sb += str_pad + util + str_pad1 + "|"
            
            sb += "\n|"
            for _ in range(NUM_COLS):
                sb += "        |"
            sb += "\n"
            
            sb += "|"
            for _ in range(NUM_COLS):
                sb += "--------|"
            sb += "\n"
        
        print(sb)
    
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
    def display_utilities_grid(util_arr):
        """
        Display the utilities of all states in a grid format.
        
        Args:
            util_arr (list): Utility values for all states.
        """
        sb = DisplayManager.frame_title("Utilities of All States (Map)")
        sb += "|"
        for _ in range(NUM_COLS):
            sb += "--------|"
        sb += "\n"
        
        for row in range(NUM_ROWS):
            sb += "|"
            for _ in range(NUM_COLS):
                sb += "        |"
            sb += "\n"
            
            sb += "|"
            for col in range(NUM_COLS):
                util = f"{util_arr[col][row].get_util():.3f}"
                sb += f" {util[:6]} |"
            
            sb += "\n|"
            for _ in range(NUM_COLS):
                sb += "        |"
            sb += "\n"
            
            sb += "|"
            for _ in range(NUM_COLS):
                sb += "--------|"
            sb += "\n"
        
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
        sb += "*" * (len(title) + 4) + "\n"
        sb += f"* {title} *\n"
        sb += "*" * (len(title) + 4) + "\n\n"
        return sb
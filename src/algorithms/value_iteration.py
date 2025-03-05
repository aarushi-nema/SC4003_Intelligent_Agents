"""
Value iteration algorithm implementation.
"""
import copy
from src.core.utility import Utility
from src.utils.constants import NUM_COLS, NUM_ROWS, DISCOUNT, EPSILON
from src.utils.utility_manager import UtilityManager
from src.utils.display_manager import DisplayManager
from src.utils.file_manager import FileManager

class ValueIteration:
    """
    Implementation of the Value Iteration algorithm.
    """
    
    def __init__(self, grid_environment):
        """
        Initialize the Value Iteration algorithm.
        
        Args:
            grid_environment: The grid environment.
        """
        self.grid_environment = grid_environment
        self.grid = grid_environment.get_grid()
        self.utility_list = []
        self.iterations = 0
        self.converge_threshold = EPSILON * ((1.0 - DISCOUNT) / DISCOUNT)
        
    def run(self):
        """
        Run the Value Iteration algorithm.
        """
        # Initialize utility arrays
        curr_util_arr = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        new_util_arr = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        
        # Initialize the utility list
        self.utility_list = []
        
        # Initialize delta
        delta = float('-inf')
        
        # Main loop
        while True:
            # Update current utilities with new utilities
            UtilityManager.update_utilities(new_util_arr, curr_util_arr)
            
            # Reset delta for this iteration
            delta = float('-inf')
            
            # Make a copy of current utilities for tracking
            curr_util_arr_copy = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
            UtilityManager.update_utilities(curr_util_arr, curr_util_arr_copy)
            self.utility_list.append(curr_util_arr_copy)
            
            # Update utilities for each state
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    # Skip walls
                    if not self.grid[col][row].is_wall:
                        # Calculate best utility for this state
                        new_util_arr[col][row] = UtilityManager.get_best_utility(
                            col, row, curr_util_arr, self.grid
                        )
                        
                        # Calculate delta
                        updated_util = new_util_arr[col][row].get_util()
                        current_util = curr_util_arr[col][row].get_util()
                        updated_delta = abs(updated_util - current_util)
                        
                        # Update delta if necessary
                        delta = max(delta, updated_delta)
            
            self.iterations += 1
            
            # Check convergence
            if delta < self.converge_threshold:
                break
        
        return self.utility_list[-1]  # Return the optimal policy
    
    def display_results(self):
        """
        Display the results of the Value Iteration algorithm.
        """
        # Get the optimal policy
        optimal_policy = self.utility_list[-1]
        
        # Display grid environment
        DisplayManager.display_grid(self.grid)
        
        # Display experiment setup
        DisplayManager.display_experiment_setup(True, self.converge_threshold)
        
        # Display iterations count
        DisplayManager.display_iterations_count(self.iterations)
        
        # Display utilities
        DisplayManager.display_utilities(self.grid, optimal_policy)
        
        # Display policy
        DisplayManager.display_policy(optimal_policy)
        
        # Display utilities grid
        DisplayManager.display_utilities_grid(optimal_policy)
        
    def save_utilities(self):
        """
        Save utility estimates to CSV file.
        """
        FileManager.write_to_file(self.utility_list, "value_iteration_utilities")
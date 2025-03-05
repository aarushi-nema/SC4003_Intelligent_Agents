"""
Policy iteration algorithm implementation.
"""
import copy
from src.core.actions import Action
from src.core.utility import Utility
from src.utils.constants import NUM_COLS, NUM_ROWS
from src.utils.utility_manager import UtilityManager
from src.utils.display_manager import DisplayManager
from src.utils.file_manager import FileManager

class PolicyIteration:
    """
    Implementation of the Policy Iteration algorithm.
    """
    
    def __init__(self, grid_environment):
        """
        Initialize the Policy Iteration algorithm.
        
        Args:
            grid_environment: The grid environment.
        """
        self.grid_environment = grid_environment
        self.grid = grid_environment.get_grid()
        self.utility_list = []
        self.iterations = 0
        
    def run(self):
        """
        Run the Policy Iteration algorithm.
        """
        # Initialize utility arrays
        curr_util_arr = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        new_util_arr = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        
        # Initialize default utilities and policies for each state
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                new_util_arr[col][row] = Utility()
                if not self.grid[col][row].is_wall:
                    random_action = Action.get_random_action()
                    new_util_arr[col][row].set_action(random_action)
        
        # Initialize the utility list
        self.utility_list = []
        
        # Flag to check if the current policy is already optimal
        unchanged = True
        
        # Main loop
        while True:
            # Update current utilities with new utilities
            UtilityManager.update_utilities(new_util_arr, curr_util_arr)
            
            # Make a copy of current utilities for tracking
            curr_util_arr_copy = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
            UtilityManager.update_utilities(curr_util_arr, curr_util_arr_copy)
            self.utility_list.append(curr_util_arr_copy)
            
            # Policy estimation based on the current actions and utilities
            new_util_arr = UtilityManager.estimate_next_utilities(curr_util_arr, self.grid)
            
            # Reset unchanged flag
            unchanged = True
            
            # Policy improvement step
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    # Skip walls
                    if not self.grid[col][row].is_wall:
                        # Calculate best action and utility
                        best_action_util = UtilityManager.get_best_utility(
                            col, row, new_util_arr, self.grid
                        )
                        
                        # Get current policy action and utility
                        policy_action = new_util_arr[col][row].get_action()
                        policy_action_util = UtilityManager.get_fixed_utility(
                            policy_action, col, row, new_util_arr, self.grid
                        )
                        
                        # Update policy if better action is found
                        if best_action_util.get_util() > policy_action_util.get_util():
                            new_util_arr[col][row].set_action(best_action_util.get_action())
                            unchanged = False
            
            self.iterations += 1
            
            # Check if policy is optimal
            if unchanged:
                break
        
        return self.utility_list[-1]  # Return the optimal policy
    
    def display_results(self):
        """
        Display the results of the Policy Iteration algorithm.
        """
        # Get the optimal policy
        optimal_policy = self.utility_list[-1]
        
        # Display grid environment
        DisplayManager.display_grid(self.grid)
        
        # Display experiment setup
        DisplayManager.display_experiment_setup(False)
        
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
        FileManager.write_to_file(self.utility_list, "policy_iteration_utilities")
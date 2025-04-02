"""
Fixed utility manager for MDP algorithms.
"""
import copy
import numpy as np
from src.core.actions import Action
from src.core.utility import Utility
from src.utils.config import NUM_COLS, NUM_ROWS, PROB_INTENT, PROB_LEFT, PROB_RIGHT, DISCOUNT, K

class UtilityManager:
    """
    Manages utilities for MDP algorithms.
    """
    
    @staticmethod
    def get_best_utility(col, row, curr_util_arr, grid):
        """
        Calculates the utility for each possible action and returns the action with maximum utility.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            Utility: The utility object with the best action and value.
        """
        utilities = []
        
        # Calculate utility for each action
        up_util = UtilityManager.get_action_up_utility(col, row, curr_util_arr, grid)
        down_util = UtilityManager.get_action_down_utility(col, row, curr_util_arr, grid)
        left_util = UtilityManager.get_action_left_utility(col, row, curr_util_arr, grid)
        right_util = UtilityManager.get_action_right_utility(col, row, curr_util_arr, grid)
        
        # Create utility objects for each action
        utilities.append(Utility(Action.UP, up_util))
        utilities.append(Utility(Action.DOWN, down_util))
        utilities.append(Utility(Action.LEFT, left_util))
        utilities.append(Utility(Action.RIGHT, right_util))
        
        # Return the action with the highest utility
        return max(utilities, key=lambda u: u.get_util())
    
    @staticmethod
    def get_fixed_utility(action, col, row, action_util_arr, grid):
        """
        Calculates the utility for the given action.
        
        Args:
            action (Action): The action to calculate utility for.
            col (int): Column index of the state.
            row (int): Row index of the state.
            action_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            Utility: The utility object with the given action and calculated value.
        """
        if action == Action.UP:
            util = UtilityManager.get_action_up_utility(col, row, action_util_arr, grid)
            return Utility(Action.UP, util)
        elif action == Action.DOWN:
            util = UtilityManager.get_action_down_utility(col, row, action_util_arr, grid)
            return Utility(Action.DOWN, util)
        elif action == Action.LEFT:
            util = UtilityManager.get_action_left_utility(col, row, action_util_arr, grid)
            return Utility(Action.LEFT, util)
        elif action == Action.RIGHT:
            util = UtilityManager.get_action_right_utility(col, row, action_util_arr, grid)
            return Utility(Action.RIGHT, util)
        
        return None
    
    @staticmethod
    def estimate_next_utilities(util_arr, grid):
        """
        Simplified Bellman update to produce the next utility estimate.
        
        Args:
            util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            list: Updated utility values for all states.
        """
        curr_util_arr = [[Utility() for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        new_util_arr = [[Utility(util_arr[col][row].get_action(), util_arr[col][row].get_util()) 
                        for row in range(NUM_ROWS)] for col in range(NUM_COLS)]
        
        k = 0
        while k < K:
            UtilityManager.update_utilities(new_util_arr, curr_util_arr)
            
            # For each state
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    if not grid[col][row].is_wall:
                        # Updates the utility based on the action stated in the policy
                        action = curr_util_arr[col][row].get_action()
                        new_util_arr[col][row] = UtilityManager.get_fixed_utility(
                            action, col, row, curr_util_arr, grid
                        )
            k += 1
            
        return new_util_arr
    
    @staticmethod
    def get_action_up_utility(col, row, curr_util_arr, grid):
        """
        Calculates the utility for attempting to move up.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value.
        """
        action_up_utility = 0.0
        
        # Intends to move up (80% probability)
        action_up_utility += PROB_INTENT * UtilityManager.move_up(col, row, curr_util_arr, grid)
        
        # Intends to move up, but moves left instead (10% probability)
        # Note: When facing up, left is to the west
        action_up_utility += PROB_LEFT * UtilityManager.move_left(col, row, curr_util_arr, grid)
        
        # Intends to move up, but moves right instead (10% probability)
        # Note: When facing up, right is to the east
        action_up_utility += PROB_RIGHT * UtilityManager.move_right(col, row, curr_util_arr, grid)
        
        # Final utility
        action_up_utility = grid[col][row].get_reward() + DISCOUNT * action_up_utility
        
        return action_up_utility
    
    @staticmethod
    def get_action_down_utility(col, row, curr_util_arr, grid):
        """
        Calculates the utility for attempting to move down.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value.
        """
        action_down_utility = 0.0
        
        # Intends to move down (80% probability)
        action_down_utility += PROB_INTENT * UtilityManager.move_down(col, row, curr_util_arr, grid)
        
        # Intends to move down, but moves right instead (10% probability)
        # Note: When facing down, right is to the west
        action_down_utility += PROB_LEFT * UtilityManager.move_right(col, row, curr_util_arr, grid)
        
        # Intends to move down, but moves left instead (10% probability)
        # Note: When facing down, left is to the east
        action_down_utility += PROB_RIGHT * UtilityManager.move_left(col, row, curr_util_arr, grid)
        
        # Final utility
        action_down_utility = grid[col][row].get_reward() + DISCOUNT * action_down_utility
        
        return action_down_utility
    
    @staticmethod
    def get_action_left_utility(col, row, curr_util_arr, grid):
        """
        Calculates the utility for attempting to move left.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value.
        """
        action_left_utility = 0.0
        
        # Intends to move left (80% probability)
        action_left_utility += PROB_INTENT * UtilityManager.move_left(col, row, curr_util_arr, grid)
        
        # Intends to move left, but moves down instead (10% probability)
        # Note: When facing left, left is to the south
        action_left_utility += PROB_LEFT * UtilityManager.move_down(col, row, curr_util_arr, grid)
        
        # Intends to move left, but moves up instead (10% probability)
        # Note: When facing left, right is to the north
        action_left_utility += PROB_RIGHT * UtilityManager.move_up(col, row, curr_util_arr, grid)
        
        # Final utility
        action_left_utility = grid[col][row].get_reward() + DISCOUNT * action_left_utility
        
        return action_left_utility
    
    @staticmethod
    def get_action_right_utility(col, row, curr_util_arr, grid):
        """
        Calculates the utility for attempting to move right.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value.
        """
        action_right_utility = 0.0
        
        # Intends to move right (80% probability)
        action_right_utility += PROB_INTENT * UtilityManager.move_right(col, row, curr_util_arr, grid)
        
        # Intends to move right, but moves up instead (10% probability)
        # Note: When facing right, left is to the north
        action_right_utility += PROB_LEFT * UtilityManager.move_up(col, row, curr_util_arr, grid)
        
        # Intends to move right, but moves down instead (10% probability)
        # Note: When facing right, right is to the south
        action_right_utility += PROB_RIGHT * UtilityManager.move_down(col, row, curr_util_arr, grid)
        
        # Final utility
        action_right_utility = grid[col][row].get_reward() + DISCOUNT * action_right_utility
        
        return action_right_utility
    
    @staticmethod
    def move_up(col, row, curr_util_arr, grid):
        """
        Attempts to move up.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value of the resulting state.
        """
        if row - 1 >= 0 and not grid[col][row - 1].is_wall:
            return curr_util_arr[col][row - 1].get_util()
        return curr_util_arr[col][row].get_util()
    
    @staticmethod
    def move_down(col, row, curr_util_arr, grid):
        """
        Attempts to move down.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value of the resulting state.
        """
        if row + 1 < NUM_ROWS and not grid[col][row + 1].is_wall:
            return curr_util_arr[col][row + 1].get_util()
        return curr_util_arr[col][row].get_util()
    
    @staticmethod
    def move_left(col, row, curr_util_arr, grid):
        """
        Attempts to move left.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value of the resulting state.
        """
        if col - 1 >= 0 and not grid[col - 1][row].is_wall:
            return curr_util_arr[col - 1][row].get_util()
        return curr_util_arr[col][row].get_util()
    
    @staticmethod
    def move_right(col, row, curr_util_arr, grid):
        """
        Attempts to move right.
        
        Args:
            col (int): Column index of the state.
            row (int): Row index of the state.
            curr_util_arr (list): Current utility values for all states.
            grid (list): The grid environment.
            
        Returns:
            float: The utility value of the resulting state.
        """
        if col + 1 < NUM_COLS and not grid[col + 1][row].is_wall:
            return curr_util_arr[col + 1][row].get_util()
        return curr_util_arr[col][row].get_util()
    
    @staticmethod
    def update_utilities(src, dest):
        """
        Copy the contents from the source array to the destination array.
        
        Args:
            src (list): Source array.
            dest (list): Destination array.
        """
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                dest[col][row] = copy.deepcopy(src[col][row])
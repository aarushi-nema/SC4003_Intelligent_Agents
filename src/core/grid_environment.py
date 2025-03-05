"""
Grid environment implementation.
"""
import numpy as np
from src.core.state import State
from src.utils.constants import (
    NUM_COLS, NUM_ROWS, WHITE_REWARD, GREEN_REWARD, 
    BROWN_REWARD, WALL_REWARD, GREEN_SQUARES, BROWN_SQUARES, WALLS_SQUARES
)

class GridEnvironment:
    """
    Represents the grid environment for the MDP.
    """
    def __init__(self):
        """
        Initialize the grid environment.
        """
        # Initialize grid with State objects
        self.grid = [[State(WHITE_REWARD) for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        self.build_grid()
        self.duplicate_grid()
        
    def get_grid(self):
        """
        Returns the actual grid.
        
        Returns:
            list: A 2D list of State objects.
        """
        return self.grid
    
    def build_grid(self):
        """
        Initialize the Grid Environment with rewards and walls.
        """
        # Set all the green squares (+1.000)
        for col, row in GREEN_SQUARES:
            self.grid[col][row].set_reward(GREEN_REWARD)
            
        # Set all the brown squares (-1.000)
        for col, row in BROWN_SQUARES:
            self.grid[col][row].set_reward(BROWN_REWARD)
            
        # Set all the walls (0.000 and unreachable, i.e., stays in the same place as before)
        for col, row in WALLS_SQUARES:
            self.grid[col][row].set_reward(WALL_REWARD)
            self.grid[col][row].set_as_wall(True)
            
    def duplicate_grid(self):
        """
        Used to 'expand' the maze if needed.
        For this implementation, we'll only support the 6x6 grid defined in constants.
        """
        pass  # Simplified for this implementation
"""
Grid environment implementation.
"""
import numpy as np
import random
from src.core.state import State
from src.utils.config import (
    NUM_COLS, NUM_ROWS, WHITE_REWARD, GREEN_REWARD, 
    BROWN_REWARD, WALL_REWARD, 
    # GREEN_SQUARES, BROWN_SQUARES, WALLS_SQUARES
)

def generate_squares_by_ratio(num_rows, num_cols, seed=None):
    """
    Generate random green, brown, and wall squares based on 6x6 ratios.
    
    Returns:
        tuple: (green_squares, brown_squares, wall_squares)
    """
    if seed is not None:
        random.seed(seed)

    total_tiles = num_rows * num_cols
    green_ratio = 6 / 36
    brown_ratio = 5 / 36
    wall_ratio = 5 / 36

    num_green = round(green_ratio * total_tiles)
    num_brown = round(brown_ratio * total_tiles)
    num_wall = round(wall_ratio * total_tiles)

    all_coords = [(col, row) for col in range(num_cols) for row in range(num_rows)]
    random.shuffle(all_coords)

    green_squares = all_coords[:num_green]
    brown_squares = all_coords[num_green:num_green + num_brown]
    wall_squares = all_coords[num_green + num_brown:num_green + num_brown + num_wall]
    print("GREEN SQUARES: ", green_squares)
    print("BROWN SQUARES: ", brown_squares)
    print("WALL SQUARES: ", wall_squares)

    return green_squares, brown_squares, wall_squares

class GridEnvironment:
    """
    Represents the grid environment for the MDP.
    """
    def __init__(self, config_module=None, use_ratios=False, seed=None):
        """
        Initialize the grid environment.
        
        Args:
            config_module: Optional configuration module to use
            use_ratios: If True, ignore config squares and generate based on 6x6 ratios
            seed: Optional seed for reproducibility
        """
        # Use provided config or default
        if config_module is None:
            from src.utils import config
            self.config = config
        else:
            self.config = config_module

        self.num_rows = self.config.NUM_ROWS
        self.num_cols = self.config.NUM_COLS

        # Initialize grid with State objects
        self.grid = [[State(self.config.WHITE_REWARD) for _ in range(self.num_rows)] 
                     for _ in range(self.num_cols)]

        if use_ratios:
            self.green_squares, self.brown_squares, self.wall_squares = generate_squares_by_ratio(
                self.num_rows, self.num_cols, seed=seed
            )
        else:
            self.green_squares = self.config.GREEN_SQUARES
            self.brown_squares = self.config.BROWN_SQUARES
            self.wall_squares = self.config.WALLS_SQUARES

        self.build_grid()

    def build_grid(self):
        """
        Initialize the Grid Environment with rewards and walls.
        """
        # Set green squares
        for col, row in self.green_squares:
            self.grid[col][row].set_reward(self.config.GREEN_REWARD)

        # Set brown squares
        for col, row in self.brown_squares:
            self.grid[col][row].set_reward(self.config.BROWN_REWARD)

        # Set wall squares
        for col, row in self.wall_squares:
            self.grid[col][row].set_reward(self.config.WALL_REWARD)
            self.grid[col][row].set_as_wall(True)

    def get_grid(self):
        """
        Returns the actual grid.
        
        Returns:
            list: A 2D list of State objects.
        """
        return self.grid

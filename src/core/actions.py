"""
Action representation and utility functions.
"""
import random
from enum import Enum

class Action(Enum):
    """
    Enumeration representing the four possible actions (UP, DOWN, LEFT, RIGHT).
    """
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    
    def __str__(self):
        """String representation of an action."""
        from src.utils.constants import ACTION_SYMBOLS
        return ACTION_SYMBOLS[self.value]
    
    @staticmethod
    def get_random_action():
        """Returns a random action."""
        return random.choice(list(Action))
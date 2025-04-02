"""
State representation for a single grid cell.
"""

class State:
    """
    Represents a single state (cell) in the grid environment.
    """
    def __init__(self, reward=0.0):
        """
        Initialize a state with a reward value.
        
        Args:
            reward (float): The reward associated with this state.
        """
        self.reward = reward
        self.is_wall = False
        
    def set_reward(self, reward):
        """
        Sets the reward value for this state.
        
        Args:
            reward (float): The new reward value.
        """
        self.reward = reward
        
    def get_reward(self):
        """
        Returns the reward value for this state.
        
        Returns:
            float: The reward value.
        """
        return self.reward
        
    def set_as_wall(self, is_wall):
        """
        Sets this state as a wall or not.
        
        Args:
            is_wall (bool): Whether this state is a wall.
        """
        self.is_wall = is_wall
        
    def is_wall(self):
        """
        Returns whether this state is a wall.
        
        Returns:
            bool: True if this state is a wall, False otherwise.
        """
        return self.is_wall
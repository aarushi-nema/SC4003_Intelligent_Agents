"""
Utility class to store an action and utility pair for a given state.
"""
from src.core.actions import Action

class Utility:
    """
    Stores an action and utility pair for a given state.
    """
    def __init__(self, action=None, util=0.0):
        """
        Initialize a utility object.
        
        Args:
            action (Action): The action associated with this utility.
            util (float): The utility value.
        """
        self.action = action
        self.util = util
        
    def get_action(self):
        """
        Returns the action.
        
        Returns:
            Action: The action.
        """
        return self.action
    
    def get_action_str(self):
        """
        Returns a string representation of the action.
        
        Returns:
            str: The string representation of the action.
        """
        if self.action is None:
            return "Wall"
        return str(self.action)
    
    def set_action(self, action):
        """
        Sets the action.
        
        Args:
            action (Action): The new action.
        """
        self.action = action
        
    def get_util(self):
        """
        Returns the utility value.
        
        Returns:
            float: The utility value.
        """
        return self.util
    
    def set_util(self, util):
        """
        Sets the utility value.
        
        Args:
            util (float): The new utility value.
        """
        self.util = util
        
    def __lt__(self, other):
        """
        Less than comparison based on utility values (used for sorting).
        
        Args:
            other (Utility): The other utility to compare with.
            
        Returns:
            bool: True if this utility is less than the other, False otherwise.
        """
        return self.util < other.util
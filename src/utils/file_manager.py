"""
File manager for saving utilities.
"""
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.constants import NUM_COLS, NUM_ROWS

class FileManager:
    """
    Manages file I/O operations.
    """
    
    @staticmethod
    def write_to_file(lst_utilities, file_name):
        """
        Write utilities to a CSV file.
        
        Args:
            lst_utilities (list): List of utility arrays.
            file_name (str): Name of the file to write to.
        """
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        rows = []
        
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                # Extract utilities for this state across all iterations
                state_utilities = [util_arr[col][row].get_util() for util_arr in lst_utilities]
                rows.append(state_utilities)
        
        # Write to CSV
        with open(f'output/{file_name}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow([f"{val:.3f}" for val in row])
        
        # Also generate the utility plot
        FileManager.plot_utilities(lst_utilities, file_name)
        
    @staticmethod
    def plot_utilities(lst_utilities, file_name):
        """
        Plot utility estimates as a function of iterations.
        
        Args:
            lst_utilities (list): List of utility arrays.
            file_name (str): Name of the file to save the plot to.
        """
        plt.figure(figsize=(12, 8))
        
        # Extract data for plot
        iterations = range(1, len(lst_utilities) + 1)
        
        # Plot utility for each state
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                label = f"State({col}, {row})"
                values = [util_arr[col][row].get_util() for util_arr in lst_utilities]
                plt.plot(iterations, values, label=label)
        
        plt.xlabel('Number of iterations')
        plt.ylabel('Utility estimates')
        plt.title('Utility Estimates as a Function of Iterations')
        plt.grid(True)
        
        # Save the plot but don't show legend as there are too many states
        # Instead, use the file to create visualizations with specific states if needed
        plt.savefig(f'output/{file_name}_plot.png')
        
        # Save selected states in another plot for better visualization
        plt.figure(figsize=(12, 8))
        
        # Only plot a few key states
        key_states = [(0, 0), (2, 0), (5, 0), (1, 1), (2, 3), (5, 5)]
        
        for col, row in key_states:
            label = f"State({col}, {row})"
            values = [util_arr[col][row].get_util() for util_arr in lst_utilities]
            plt.plot(iterations, values, label=label, linewidth=2)
        
        plt.xlabel('Number of iterations')
        plt.ylabel('Utility estimates')
        plt.title('Utility Estimates for Key States')
        plt.grid(True)
        plt.legend()
        plt.savefig(f'output/{file_name}_key_states_plot.png')
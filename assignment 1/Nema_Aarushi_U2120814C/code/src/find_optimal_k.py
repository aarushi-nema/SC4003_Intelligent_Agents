"""
Experiment to find optimal K value for Policy Iteration with multiple runs.
This script runs Policy Iteration 10 times for each K value and records statistical results.
"""
import os
import sys
import time
import copy
import matplotlib.pyplot as plt
import numpy as np
from src.core.grid_environment import GridEnvironment
from src.algorithms.policy_iteration import PolicyIteration
from src.utils.grid_visualizer import GridVisualizer

# Define output directory - use a relative path that works on your system
output_dir = r'C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\part_1_results\find_optimal_k_multiple'
os.makedirs(output_dir, exist_ok=True)

# Range of K values to test
k_values = [25, 50, 75, 100, 125]
num_runs = 10  # Number of runs for each K value

# Results storage
results = {k: {
    'iterations': [],
    'avg_utility': [],
    'max_utility': [],
    'execution_time': [],
} for k in k_values}

# Summary results storage
summary = {k: {
    'iterations_min': 0, 'iterations_max': 0,
    'avg_utility_min': 0.0, 'avg_utility_max': 0.0,
    'max_utility_min': 0.0, 'max_utility_max': 0.0,
    'time_min': 0.0, 'time_max': 0.0,
} for k in k_values}

print("\n" + "="*50)
print(f"K-Value Experiment for Policy Iteration ({num_runs} runs per K value)")
print("="*50)

# Run policy iteration for each K value
for k in k_values:
    print(f"\nTesting K = {k}")
    
    for run in range(1, num_runs + 1):
        print(f"  Run {run}/{num_runs}...")
        
        # Create a new grid environment for each run
        grid_environment = GridEnvironment()
        grid = grid_environment.get_grid()
        
        # Temporarily modify the K value in config
        import src.utils.config
        original_k = src.utils.config.K
        src.utils.config.K = k
        
        # Start timing
        start_time = time.time()
        
        # Run policy iteration with current K value
        pi = PolicyIteration(grid_environment)
        optimal_policy = pi.run()
        
        # End timing
        execution_time = time.time() - start_time
        
        # Calculate statistics
        utilities = []
        for col in range(len(grid)):
            for row in range(len(grid[0])):
                if not grid[col][row].is_wall:
                    utilities.append(optimal_policy[col][row].get_util())
        
        avg_utility = sum(utilities) / len(utilities)
        max_utility = max(utilities)
        
        # Store results
        results[k]['iterations'].append(pi.iterations)
        results[k]['avg_utility'].append(avg_utility)
        results[k]['max_utility'].append(max_utility)
        results[k]['execution_time'].append(execution_time)
        
        # Reset K to original value
        src.utils.config.K = original_k
    
    # Calculate summary statistics for this K value
    summary[k]['iterations_min'] = min(results[k]['iterations'])
    summary[k]['iterations_max'] = max(results[k]['iterations'])
    summary[k]['avg_utility_min'] = min(results[k]['avg_utility'])
    summary[k]['avg_utility_max'] = max(results[k]['avg_utility'])
    summary[k]['max_utility_min'] = min(results[k]['max_utility'])
    summary[k]['max_utility_max'] = max(results[k]['max_utility'])
    summary[k]['time_min'] = min(results[k]['execution_time'])
    summary[k]['time_max'] = max(results[k]['execution_time'])
    
    # Print summary for this K value
    print(f"\nFor K={k}")
    print(f"# of iterations = {summary[k]['iterations_min']} to {summary[k]['iterations_max']}")
    print(f"Average utility = {summary[k]['avg_utility_min']:.2f} to {summary[k]['avg_utility_max']:.2f}")
    print(f"Maximum Utility = {summary[k]['max_utility_min']:.2f} to {summary[k]['max_utility_max']:.2f}")
    print(f"Time to converge: {summary[k]['time_min']:.2f} to {summary[k]['time_max']:.2f} seconds")

# Save detailed results to a CSV file
import csv
csv_path = os.path.join(output_dir, 'k_experiment_detailed_results.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    header = ['k', 'run', 'iterations', 'avg_utility', 'max_utility', 'execution_time']
    writer.writerow(header)
    
    for k in k_values:
        for run in range(num_runs):
            writer.writerow([
                k,
                run + 1,
                results[k]['iterations'][run],
                results[k]['avg_utility'][run],
                results[k]['max_utility'][run],
                results[k]['execution_time'][run]
            ])

# Save summary results to a CSV file
csv_summary_path = os.path.join(output_dir, 'k_experiment_summary_results.csv')
with open(csv_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    header = [
        'k', 
        'iterations_min', 'iterations_max',
        'avg_utility_min', 'avg_utility_max',
        'max_utility_min', 'max_utility_max',
        'time_min', 'time_max'
    ]
    writer.writerow(header)
    
    for k in k_values:
        writer.writerow([
            k,
            summary[k]['iterations_min'],
            summary[k]['iterations_max'],
            summary[k]['avg_utility_min'],
            summary[k]['avg_utility_max'],
            summary[k]['max_utility_min'],
            summary[k]['max_utility_max'],
            summary[k]['time_min'],
            summary[k]['time_max']
        ])

# Save a summary text report
report_path = os.path.join(output_dir, 'k_experiment_summary_report.txt')
with open(report_path, 'w') as f:
    f.write("="*50 + "\n")
    f.write(f"K-Value Experiment for Policy Iteration ({num_runs} runs per K value)\n")
    f.write("="*50 + "\n\n")
    
    for k in k_values:
        f.write(f"For K={k}\n")
        f.write(f"# of iterations = {summary[k]['iterations_min']} to {summary[k]['iterations_max']}\n")
        f.write(f"Average utility = {summary[k]['avg_utility_min']:.2f} to {summary[k]['avg_utility_max']:.2f}\n")
        f.write(f"Maximum Utility = {summary[k]['max_utility_min']:.2f} to {summary[k]['max_utility_max']:.2f}\n")
        f.write(f"Time to converge: {summary[k]['time_min']:.2f} to {summary[k]['time_max']:.2f} seconds\n\n")
    
    # Calculate best K based on average of max utilities across runs
    avg_max_utility = {k: sum(results[k]['max_utility']) / len(results[k]['max_utility']) for k in k_values}
    best_k = max(avg_max_utility, key=avg_max_utility.get)
    
    f.write("="*50 + "\n")
    f.write("Overall Recommendation\n")
    f.write("="*50 + "\n\n")
    f.write(f"Based on average maximum utility across {num_runs} runs:\n")
    f.write(f"Recommended K value: {best_k}\n")
    f.write(f"Average maximum utility: {avg_max_utility[best_k]:.4f}\n")

# Create box plots for different metrics
plt.figure(figsize=(15, 10))

# Iterations box plot
plt.subplot(2, 2, 1)
data = [results[k]['iterations'] for k in k_values]
plt.boxplot(data, labels=k_values)
plt.title('Total Iterations Distribution by K Value')
plt.xlabel('K Value')
plt.ylabel('Iterations')
plt.grid(True, linestyle='--', alpha=0.7)

# Average Utility box plot
plt.subplot(2, 2, 2)
data = [results[k]['avg_utility'] for k in k_values]
plt.boxplot(data, labels=k_values)
plt.title('Average Utility Distribution by K Value')
plt.xlabel('K Value')
plt.ylabel('Average Utility')
plt.grid(True, linestyle='--', alpha=0.7)

# Maximum Utility box plot
plt.subplot(2, 2, 3)
data = [results[k]['max_utility'] for k in k_values]
plt.boxplot(data, labels=k_values)
plt.title('Maximum Utility Distribution by K Value')
plt.xlabel('K Value')
plt.ylabel('Maximum Utility')
plt.grid(True, linestyle='--', alpha=0.7)

# Execution Time box plot
plt.subplot(2, 2, 4)
data = [results[k]['execution_time'] for k in k_values]
plt.boxplot(data, labels=k_values)
plt.title('Execution Time Distribution by K Value')
plt.xlabel('K Value')
plt.ylabel('Time (seconds)')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'k_value_comparison_boxplots.png'))

print("\n" + "="*50)
print("Multiple Run Experiment Completed")
print("="*50)
print(f"Results saved to {output_dir}")

# Calculate and print the overall best K value
avg_max_utility = {k: sum(results[k]['max_utility']) / len(results[k]['max_utility']) for k in k_values}
best_k = max(avg_max_utility, key=avg_max_utility.get)

print(f"\nBased on average maximum utility across {num_runs} runs:")
print(f"Recommended K value: {best_k}")
print(f"Average maximum utility: {avg_max_utility[best_k]:.4f}")
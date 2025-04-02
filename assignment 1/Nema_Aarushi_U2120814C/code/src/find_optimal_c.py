"""
Experiment to find optimal EPSILON (c) value for Value Iteration.
This script runs Value Iteration with different EPSILON values and records the results.
"""
import os
import sys
import time
import copy
import matplotlib.pyplot as plt
import numpy as np
from src.core.grid_environment import GridEnvironment
from src.algorithms.value_iteration import ValueIteration
from src.utils.config import DISCOUNT

# Create directory for experiment results
os.makedirs(r'C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\part_1_results\find_optimal_c', exist_ok=True)

# Range of EPSILON values to test
epsilon_values = [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 20.0, 40.0, 60.0]

# Results storage
results = {
    'epsilon': [],
    'iterations': [],
    'avg_utility': [],
    'max_utility': [],
    'execution_time': [],
    'converge_threshold': []
}

print("\n" + "="*50)
print("EPSILON Experiment for Value Iteration")
print("="*50)

# Create grid environment
grid_environment = GridEnvironment()
grid = grid_environment.get_grid()

# Run value iteration for each EPSILON value
for epsilon in epsilon_values:
    print(f"\nTesting EPSILON = {epsilon}")
    
    # Create a modified ValueIteration class that uses our custom EPSILON
    class ModifiedValueIteration(ValueIteration):
        def __init__(self, grid_environment, custom_epsilon):
            super().__init__(grid_environment)
            # Override the converge threshold with our custom EPSILON
            self.converge_threshold = custom_epsilon * ((1.0 - DISCOUNT) / DISCOUNT)
            print(f"  Convergence threshold: {self.converge_threshold:.8f}")
    
    # Start timing
    start_time = time.time()
    
    # Run value iteration with current EPSILON
    vi = ModifiedValueIteration(grid_environment, epsilon)
    optimal_policy = vi.run()
    # End timing
    execution_time = time.time() - start_time
    # vi.display_results()
    vi.save_utilities()
    try:
        # Import here to avoid issues if matplotlib is not installed
        from src.utils.grid_visualizer import GridVisualizer
        
        print("\nGenerating Value Iteration visualization...")
        GridVisualizer.visualize_policy_grid(
            grid_environment.get_grid(), 
            optimal_policy,
            "Value Iteration: Optimal Policy and Utilities",
            path=r'C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\part_1_results\find_optimal_c',
            filename=f"{epsilon}value_iteration_policy.png",
        )
    except ImportError as e:
        print(f"Error importing visualization module: {e}")
        print("Make sure matplotlib and numpy are installed.")
    except Exception as e:
        print(f"Error generating visualization: {e}")
    
    # Calculate statistics
    utilities = []
    for col in range(len(grid)):
        for row in range(len(grid[0])):
            if not grid[col][row].is_wall:
                utilities.append(optimal_policy[col][row].get_util())
    
    avg_utility = sum(utilities) / len(utilities)
    max_utility = max(utilities)
    
    # Store results
    results['epsilon'].append(epsilon)
    results['iterations'].append(vi.iterations)
    results['avg_utility'].append(avg_utility)
    results['max_utility'].append(max_utility)
    results['execution_time'].append(execution_time)
    results['converge_threshold'].append(vi.converge_threshold)
    
    print(f"  Iterations: {vi.iterations}")
    print(f"  Average utility: {avg_utility:.4f}")
    print(f"  Maximum utility: {max_utility:.4f}")
    print(f"  Execution time: {execution_time:.4f} seconds")
    
    # Save the utility grid to a file for this EPSILON value
    filename = rf"C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\part_1_results\find_optimal_c\{epsilon}_utilities.txt"
    with open(filename, 'w') as f:
        f.write(f"EPSILON = {epsilon}\n")
        f.write(f"Avg Utility = {avg_utility}\n")
        f.write(f"Max Utility = {max_utility}\n")
        f.write(f"Max Utility = {max_utility}\n")
        f.write(f"Execution time = {execution_time}\n")
        f.write(f"Iterations = {vi.iterations}\n\n")
        f.write("Utilities Grid:\n")
        for row in range(len(grid[0])):
            for col in range(len(grid)):
                util = optimal_policy[col][row].get_util()
                f.write(f"{util:.4f}\t")
            f.write("\n")

# Create visualizations of the results
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(results['epsilon'], results['iterations'], 'o-')
plt.xscale('log')
plt.title('Iterations vs EPSILON')
plt.xlabel('EPSILON (log scale)')
plt.ylabel('Number of Iterations')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(results['epsilon'], results['avg_utility'], 'o-')
plt.xscale('log')
plt.title('Average Utility vs EPSILON')
plt.xlabel('EPSILON (log scale)')
plt.ylabel('Average Utility')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(results['epsilon'], results['max_utility'], 'o-')
plt.xscale('log')
plt.title('Maximum Utility vs EPSILON')
plt.xlabel('EPSILON (log scale)')
plt.ylabel('Maximum Utility')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(results['epsilon'], results['execution_time'], 'o-')
plt.xscale('log')
plt.title('Execution Time vs EPSILON')
plt.xlabel('EPSILON (log scale)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True)

plt.tight_layout()
plt.savefig('experiments/epsilon/epsilon_experiment_results.png')

# Save results to a CSV file
import csv
with open('experiments/epsilon/epsilon_experiment_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['epsilon', 'iterations', 'avg_utility', 'max_utility', 'execution_time', 'converge_threshold'])
    for i in range(len(results['epsilon'])):
        writer.writerow([
            results['epsilon'][i],
            results['iterations'][i],
            results['avg_utility'][i],
            results['max_utility'][i],
            results['execution_time'][i],
            results['converge_threshold'][i]
        ])

print("\n" + "="*50)
print("Experiment Completed")
print("="*50)
print(f"Results saved to experiments/epsilon/ directory")

# Find and print the optimal EPSILON value based on maximum utility
max_utility_index = results['max_utility'].index(max(results['max_utility']))
max_avg_utility_index = results['avg_utility'].index(max(results['avg_utility']))

print(f"\nBased on maximum utility:")
print(f"  Optimal EPSILON: {results['epsilon'][max_utility_index]}")
print(f"  Maximum utility: {results['max_utility'][max_utility_index]}")
print(f"  Iterations: {results['iterations'][max_utility_index]}")

print(f"\nBased on average utility:")
print(f"  Optimal EPSILON: {results['epsilon'][max_avg_utility_index]}")
print(f"  Average utility: {results['avg_utility'][max_avg_utility_index]}")
print(f"  Iterations: {results['iterations'][max_avg_utility_index]}")

# Create a plot showing the tradeoff between utility and iterations
plt.figure(figsize=(10, 6))
plt.scatter(results['iterations'], results['avg_utility'], 
           s=100, c=np.log(results['epsilon']), cmap='viridis', 
           alpha=0.7, edgecolors='black', linewidths=1)

for i, eps in enumerate(results['epsilon']):
    plt.annotate(f"ε={eps}", 
                (results['iterations'][i], results['avg_utility'][i]),
                xytext=(5, 5), textcoords='offset points')

plt.colorbar(label='log(EPSILON)')
plt.title('Tradeoff: Average Utility vs. Iterations')
plt.xlabel('Number of Iterations')
plt.ylabel('Average Utility')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('experiments/epsilon/utility_vs_iterations_tradeoff.png')

print("\nTradeoff plot saved to experiments/epsilon/utility_vs_iterations_tradeoff.png")
"""
Main entry point for the MDP solution with initial grid visualization.
"""
import argparse
import os
import time
import sys
from src.core.grid_environment import GridEnvironment
from src.algorithms.value_iteration import ValueIteration
from src.algorithms.policy_iteration import PolicyIteration
from src.utils.config import (
    NUM_COLS, NUM_ROWS
)

def main():
    """
    Main entry point.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MDP solution with Value Iteration and Policy Iteration')
    parser.add_argument('--algorithm', type=str, default='both',
                        choices=['value', 'policy', 'both'],
                        help='Algorithm to run (value, policy, or both)')
    parser.add_argument('--visualize', action='store_true',
                        help='Generate visualizations of the results')
    parser.add_argument('--no-visualize', action='store_true',
                    help='Disable visualizations')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Create grid environment
    grid_environment = GridEnvironment(use_ratios=True, seed=42)
    print("GRID ENV CREATED")
    
    # Visualize initial grid if requested
    # if args.visualize or args.initial_only:
    if (args.visualize or getattr(args, 'initial_only', False)) and not args.no_visualize:
        try:
            from src.utils.initial_grid_visualizer import InitialGridVisualizer
            
            print("\nGenerating initial grid visualization...")
            InitialGridVisualizer.visualize_initial_grid(
                grid_environment.get_grid(), 
                "Initial Grid Environment (Before Algorithms)",
                "initial_grid_environment.png"
            )
            
            # If only initial visualization was requested, exit
            # if args.initial_only:
            if getattr(args, 'initial_only', False):
                print("Initial grid visualization complete. Exiting as requested.")
                return
                
        except ImportError as e:
            print(f"Error importing visualization module: {e}")
            print("Make sure matplotlib and numpy are installed.")
        except Exception as e:
            print(f"Error generating initial visualization: {e}")
    
    # Store optimal policies for visualization
    value_policy = None
    policy_policy = None
    

    with open(r"C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\algorithm_performance.txt", 'a') as file:
        file.write(f"\n-----------------------------------------------------------------------")
        file.write(f"\n\n{NUM_ROWS}x{NUM_COLS} Grid")
    
    # Run selected algorithm(s)
    if args.algorithm in ['value', 'both']:
        print("\n" + "="*50)
        print("Running Value Iteration")
        print("="*50)
        
        value_iteration = ValueIteration(grid_environment)
        # value_policy = value_iteration.run()
        start_time = time.time()
        value_policy  = value_iteration.run()
        end_time = time.time()
        elapsed_time = end_time - start_time
        # results.append(f"Value Iteration | Time: {elapsed_time:.4f}s")
        with open(r"C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\algorithm_performance.txt", 'a') as file:
            file.write(f"\n***** Value Iteration ***** \n----- Time Elapsed ----- \nTime: {elapsed_time:.4f}s")
        value_iteration.display_results()
        value_iteration.save_utilities()
        
        # Generate visualization if requested
        # if args.visualize:
        if args.visualize and not args.no_visualize:
            try:
                # Import here to avoid issues if matplotlib is not installed
                from src.utils.grid_visualizer import GridVisualizer
                
                print("\nGenerating Value Iteration visualization...")
                GridVisualizer.visualize_policy_grid(
                    grid_environment.get_grid(), 
                    value_policy,
                    "Value Iteration: Optimal Policy and Utilities",
                    "value_iteration_policy.png"
                )
            except ImportError as e:
                print(f"Error importing visualization module: {e}")
                print("Make sure matplotlib and numpy are installed.")
            except Exception as e:
                print(f"Error generating visualization: {e}")
    
    if args.algorithm in ['policy', 'both']:
        print("\n" + "="*50)
        print("Running Policy Iteration")
        print("="*50)
        
        policy_iteration = PolicyIteration(grid_environment)

        start_time = time.time()
        policy_policy = policy_iteration.run()
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time = end_time - start_time
        # results.append(f"Value Iteration | Time: {elapsed_time:.4f}s")
        with open(r"C:\Users\Aarushi\Desktop\SC4003_Intelligent_Agents\output\algorithm_performance.txt", 'a') as file:
            file.write(f"\n***** Policy Iteration ***** \n----- Time Elapsed ----- \nTime: {elapsed_time:.4f}s")
        
        policy_iteration.display_results()
        policy_iteration.save_utilities()
        
        # Generate visualization if requested
        # if args.visualize:
        if args.visualize and not args.no_visualize:
            try:
                # Import here to avoid issues if matplotlib is not installed
                from src.utils.grid_visualizer import GridVisualizer
                
                print("\nGenerating Policy Iteration visualization...")
                GridVisualizer.visualize_policy_grid(
                    grid_environment.get_grid(), 
                    policy_policy,
                    "Policy Iteration: Optimal Policy and Utilities",
                    "policy_iteration_policy.png"
                )
            except ImportError as e:
                print(f"Error importing visualization module: {e}")
                print("Make sure matplotlib and numpy are installed.")
            except Exception as e:
                print(f"Error generating visualization: {e}")
    
    # If both algorithms were run and visualization is requested, create a comparison
    # if args.algorithm == 'both' and args.visualize and value_policy and policy_policy:
    if args.algorithm == 'both' and args.visualize and not args.no_visualize and value_policy and policy_policy:
        try:
            from src.utils.grid_visualizer import GridVisualizer
            
            print("\nGenerating comparison visualization...")
            GridVisualizer.compare_policies(
                grid_environment.get_grid(),
                value_policy,
                policy_policy,
                "Comparison: Value Iteration vs Policy Iteration",
                "policy_comparison.png"
            )
        except ImportError as e:
            print(f"Error importing visualization module: {e}")
            print("Make sure matplotlib and numpy are installed.")
        except Exception as e:
            print(f"Error generating comparison visualization: {e}")


if __name__ == "__main__":
    main()
"""
Main entry point for the MDP solution.
"""
import argparse
from src.core.grid_environment import GridEnvironment
from src.algorithms.value_iteration import ValueIteration
from src.algorithms.policy_iteration import PolicyIteration

def main():
    """
    Main entry point.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MDP solution with Value Iteration and Policy Iteration')
    parser.add_argument('--algorithm', type=str, default='both',
                        choices=['value', 'policy', 'both'],
                        help='Algorithm to run (value, policy, or both)')
    
    args = parser.parse_args()
    
    # Create grid environment
    grid_environment = GridEnvironment()
    
    # Run selected algorithm(s)
    if args.algorithm in ['value', 'both']:
        print("\n" + "="*50)
        print("Running Value Iteration")
        print("="*50)
        
        value_iteration = ValueIteration(grid_environment)
        value_iteration.run()
        value_iteration.display_results()
        value_iteration.save_utilities()
    
    if args.algorithm in ['policy', 'both']:
        print("\n" + "="*50)
        print("Running Policy Iteration")
        print("="*50)
        
        policy_iteration = PolicyIteration(grid_environment)
        policy_iteration.run()
        policy_iteration.display_results()
        policy_iteration.save_utilities()

if __name__ == "__main__":
    main()
"""
Constants used throughout the project.
"""

# Size of the Grid World
NUM_COLS = 6
NUM_ROWS = 6

# Reward functions
WHITE_REWARD = -0.040
GREEN_REWARD = 1.000
BROWN_REWARD = -1.000
WALL_REWARD = 0.000

# Transition model
PROB_INTENT = 0.800
PROB_LEFT = 0.100
PROB_RIGHT = 0.100

# Grid Environment information
# Format: list of (col, row) tuples
GREEN_SQUARES = [(0, 0), (2, 0), (5, 0), (3, 1), (4, 2), (5, 3)]
BROWN_SQUARES = [(1, 1), (5, 1), (2, 2), (3, 3), (4, 4)]
WALLS_SQUARES = [(1, 0), (4, 1), (1, 4), (2, 4), (3, 4)]

# Agent's starting position
# NOTE: A remarkable consequence of using discounted utilities with infinite
# horizons is that the optimal policy is independent of the starting state
AGENT_START_COL = 2  # first col starts from 0
AGENT_START_ROW = 3  # first row starts from 0

# Discount factor
DISCOUNT = 0.990

# Rmax (maximum reward)
R_MAX = 1.000

# Constant c (parameter to adjust the maximum error allowed)
C = 30.0

# Epsilon = c * Rmax (maximum error allowed in the utility of any state)
EPSILON = C * R_MAX

# Utility upper bound
UTILITY_UPPER_BOUND = R_MAX / (1 - DISCOUNT)

# Constant k (number of times simplified Bellman update is executed
# to produce the next utility estimate in policy iteration)
K = 10

# Action symbols for display
ACTION_SYMBOLS = {
    "UP": "^",
    "DOWN": "v",
    "LEFT": "<",
    "RIGHT": ">",
    "WALL": "Wall"
}
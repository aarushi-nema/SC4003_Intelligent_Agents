public class NashEquilibriumAnalyzer {
    private OptimizeStrategy gameEnvironment;
    private int totalStrategies;
    private float[][][] payoffMatrix; // [player1Strategy][player2Strategy][player3Strategy]
    
    public NashEquilibriumAnalyzer(OptimizeStrategy gameEnv) {
        this.gameEnvironment = gameEnv;
        this.totalStrategies = gameEnv.numPlayers;
        
        // Initialize payoff matrix
        initializePayoffMatrix();
    }
    
    private void initializePayoffMatrix() {
        payoffMatrix = new float[totalStrategies][totalStrategies][totalStrategies];
        
        // Calculate payoffs for all strategy combinations
        for (int i = 0; i < totalStrategies; i++) {
            for (int j = 0; j < totalStrategies; j++) {
                for (int k = 0; k < totalStrategies; k++) {
                    OptimizeStrategy.Player playerA = gameEnvironment.makePlayer(i);
                    OptimizeStrategy.Player playerB = gameEnvironment.makePlayer(j);
                    OptimizeStrategy.Player playerC = gameEnvironment.makePlayer(k);
                    
                    // Run multiple matches to get average payoffs
                    float[] avgPayoffs = calculateAveragePayoffs(playerA, playerB, playerC);
                    
                    // Store in payoff matrix
                    payoffMatrix[i][j][k] = avgPayoffs[0]; // Player A's payoff
                    payoffMatrix[j][k][i] = avgPayoffs[1]; // Player B's payoff 
                    payoffMatrix[k][i][j] = avgPayoffs[2]; // Player C's payoff
                }
            }
        }
    }
    
    private float[] calculateAveragePayoffs(OptimizeStrategy.Player A, OptimizeStrategy.Player B, 
                                           OptimizeStrategy.Player C) {
        float[] totalPayoffs = {0, 0, 0};
        int matchCount = 10; // Run multiple matches for statistical reliability
        
        for (int m = 0; m < matchCount; m++) {
            int rounds = 90 + (int)Math.rint(20 * Math.random()); // Between 90-110 rounds
            float[] matchPayoffs = gameEnvironment.scoresOfMatch(A, B, C, rounds);
            
            // Accumulate payoffs
            totalPayoffs[0] += matchPayoffs[0];
            totalPayoffs[1] += matchPayoffs[1];
            totalPayoffs[2] += matchPayoffs[2];
        }
        
        // Calculate averages
        totalPayoffs[0] /= matchCount;
        totalPayoffs[1] /= matchCount;
        totalPayoffs[2] /= matchCount;
        
        return totalPayoffs;
    }
    
    public boolean isNashEquilibrium(int player1Strat, int player2Strat, int player3Strat) {
        // Check if player 1 has any profitable deviation
        float currentPayoff1 = payoffMatrix[player1Strat][player2Strat][player3Strat];
        for (int i = 0; i < totalStrategies; i++) {
            if (i != player1Strat && payoffMatrix[i][player2Strat][player3Strat] > currentPayoff1) {
                return false; // Player 1 has a profitable deviation
            }
        }
        
        // Check if player 2 has any profitable deviation
        float currentPayoff2 = payoffMatrix[player2Strat][player3Strat][player1Strat];
        for (int j = 0; j < totalStrategies; j++) {
            if (j != player2Strat && payoffMatrix[player2Strat][j][player1Strat] > currentPayoff2) {
                return false; // Player 2 has a profitable deviation
            }
        }
        
        // Check if player 3 has any profitable deviation
        float currentPayoff3 = payoffMatrix[player3Strat][player1Strat][player2Strat];
        for (int k = 0; k < totalStrategies; k++) {
            if (k != player3Strat && payoffMatrix[player3Strat][player1Strat][k] > currentPayoff3) {
                return false; // Player 3 has a profitable deviation
            }
        }
        
        // If no player has a profitable deviation, this is a Nash equilibrium
        return true;
    }
    
    public void findAllNashEquilibria() {
        System.out.println("Nash Equilibria in the Three-Player Prisoner's Dilemma:");
        int equilibriumCount = 0;
        
        for (int i = 0; i < totalStrategies; i++) {
            for (int j = 0; j < totalStrategies; j++) {
                for (int k = 0; k < totalStrategies; k++) {
                    if (isNashEquilibrium(i, j, k)) {
                        equilibriumCount++;
                        System.out.println("Equilibrium " + equilibriumCount + ": (" + 
                                           gameEnvironment.makePlayer(i).name() + ", " +
                                           gameEnvironment.makePlayer(j).name() + ", " +
                                           gameEnvironment.makePlayer(k).name() + ")");
                    }
                }
            }
        }
        
        if (equilibriumCount == 0) {
            System.out.println("No pure strategy Nash equilibria found.");
        }
    }

    // Get payoffs for a specific strategy profile
public float[] getEquilibriumPayoffs(int player1Strat, int player2Strat, int player3Strat) {
    float[] payoffs = new float[3];
    payoffs[0] = payoffMatrix[player1Strat][player2Strat][player3Strat];
    payoffs[1] = payoffMatrix[player2Strat][player3Strat][player1Strat];
    payoffs[2] = payoffMatrix[player3Strat][player1Strat][player2Strat];
    return payoffs;
}

// Find best responses for each player
public int[][] findBestResponses(int player1Strat, int player2Strat, int player3Strat) {
    int[][] bestResponses = new int[3][3]; // [player][bestStrategy, currentPayoff, newPayoff]
    
    // For player 1
    float currentPayoff1 = payoffMatrix[player1Strat][player2Strat][player3Strat];
    float bestPayoff1 = currentPayoff1;
    int bestStrategy1 = player1Strat;
    
    for (int i = 0; i < totalStrategies; i++) {
        if (i != player1Strat) {
            float payoff = payoffMatrix[i][player2Strat][player3Strat];
            if (payoff > bestPayoff1) {
                bestPayoff1 = payoff;
                bestStrategy1 = i;
            }
        }
    }
    
    bestResponses[0][0] = bestStrategy1;
    bestResponses[0][1] = (int)currentPayoff1;
    bestResponses[0][2] = (int)bestPayoff1;
    
    // Repeat for players 2 and 3 (similar structure)
    // ...
    
    return bestResponses;
}

// Getter for the payoff matrix
public float[][][] getPayoffMatrix() {
    return payoffMatrix;
}
}
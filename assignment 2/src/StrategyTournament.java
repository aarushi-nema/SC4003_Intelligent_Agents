public class StrategyTournament {
    public static void main(String[] args) {
        System.out.println("Starting Three Prisoner's Dilemma Tournament");
        System.out.println("===========================================");
        
        // Create an instance of the dilemma
        OptimizeStrategy tpd = new OptimizeStrategy();
        
        // Run multiple tournaments for more reliable results
        int numTournaments = 5;
        float[][] allScores = new float[numTournaments][];
        
        // Get player names once
        String[] playerNames = new String[tpd.numPlayers];
        for (int i = 0; i < tpd.numPlayers; i++) {
            playerNames[i] = tpd.makePlayer(i).name();
        }
        
        // Run the tournaments
        for (int i = 0; i < numTournaments; i++) {
            System.out.println("\nRunning tournament " + (i+1) + " of " + numTournaments);
            
            // For non-first tournaments, we'll silence output by redirecting System.out
            java.io.PrintStream originalOut = System.out;
            if (i > 0) {
                // Redirect System.out to a dummy PrintStream (only for non-first tournament)
                System.setOut(new java.io.PrintStream(new java.io.OutputStream() {
                    public void write(int b) { /* Do nothing */ }
                }));
            }
            
            // Run tournament and collect scores
            allScores[i] = runTournamentAndGetScores(tpd);
            
            // Restore original System.out if we redirected it
            if (i > 0) {
                System.setOut(originalOut);
            }
            
            // Print the scores for this tournament
            System.out.println("\nResults of tournament " + (i+1) + ":");
            printResults(playerNames, allScores[i], false);
        }
        
        // Calculate average scores across all tournaments
        float[] avgScores = new float[tpd.numPlayers];
        for (int i = 0; i < tpd.numPlayers; i++) {
            for (int j = 0; j < numTournaments; j++) {
                avgScores[i] += allScores[j][i];
            }
            avgScores[i] /= numTournaments;
        }
        
        // Print final averaged results
        System.out.println("\n\nFINAL RESULTS (Average of " + numTournaments + " tournaments):");
        System.out.println("=================================================");
        printResults(playerNames, avgScores, true);
        
        // Compare against Nema_Aarushi_Player specifically
        compareToNemaPlayer(playerNames, avgScores);

        // GameTheoryAnalyzer.analyze();
    }
    
    // Implementation of runTournamentAndGetScores
    private static float[] runTournamentAndGetScores(OptimizeStrategy tpd) {
        float[] totalScore = new float[tpd.numPlayers];

        // This loop plays each triple of players against each other
        for (int i=0; i<tpd.numPlayers; i++) 
            for (int j=i; j<tpd.numPlayers; j++) 
                for (int k=j; k<tpd.numPlayers; k++) {
                    OptimizeStrategy.Player A = tpd.makePlayer(i);
                    OptimizeStrategy.Player B = tpd.makePlayer(j);
                    OptimizeStrategy.Player C = tpd.makePlayer(k);
                    int rounds = 90 + (int)Math.rint(20 * Math.random()); // Between 90 and 110 rounds
                    float[] matchResults = tpd.scoresOfMatch(A, B, C, rounds);
                    totalScore[i] += matchResults[0];
                    totalScore[j] += matchResults[1];
                    totalScore[k] += matchResults[2];
                }
        
        return totalScore;
    }
    
    private static void printResults(String[] playerNames, float[] scores, boolean sort) {
        // Create an array of indices
        Integer[] indices = new Integer[playerNames.length];
        for (int i = 0; i < indices.length; i++) {
            indices[i] = i;
        }
        
        // Sort if requested
        if (sort) {
            java.util.Arrays.sort(indices, (a, b) -> Float.compare(scores[b], scores[a]));
        }
        
        // Print the results
        for (int i = 0; i < indices.length; i++) {
            int idx = indices[i];
            System.out.printf("%2d. %-30s: %.2f points\n", (i+1), playerNames[idx], scores[idx]);
        }
    }
    
    private static void compareToNemaPlayer(String[] playerNames, float[] scores) {
        // Find Nema_Aarushi_Player index
        int nemaIndex = -1;
        for (int i = 0; i < playerNames.length; i++) {
            if (playerNames[i].contains("Nema_Aarushi_Player")) {
                nemaIndex = i;
                break;
            }
        }
        
        if (nemaIndex == -1) {
            System.out.println("\nCould not find Nema_Aarushi_Player for comparison");
            return;
        }
        
        float nemaScore = scores[nemaIndex];
        
        System.out.println("\nDetailed Comparison with Nema_Aarushi_Player:");
        System.out.println("=============================================");
        System.out.printf("Nema_Aarushi_Player score: %.2f points\n\n", nemaScore);
        
        // Create an array of indices excluding Nema player
        Integer[] indices = new Integer[playerNames.length - 1];
        int idx = 0;
        for (int i = 0; i < playerNames.length; i++) {
            if (i != nemaIndex) {
                indices[idx++] = i;
            }
        }
        
        // Sort by performance difference
        java.util.Arrays.sort(indices, (a, b) -> {
            float diffA = nemaScore - scores[a];
            float diffB = nemaScore - scores[b];
            return Float.compare(diffA, diffB);
        });
        
        // Print comparisons
        System.out.println("Nema_Aarushi_Player compared to other strategies:");
        for (int i = 0; i < indices.length; i++) {
            int strategyIdx = indices[i];
            float diff = nemaScore - scores[strategyIdx];
            String status;
            
            if (Math.abs(diff) < 1.0) {
                status = "performs similarly to";
            } else if (diff < 0) {
                status = String.format("underperforms by %.2f points compared to", -diff);
            } else {
                status = String.format("outperforms by %.2f points compared to", diff);
            }
            
            System.out.printf("- Nema_Aarushi_Player %s %s (%.2f points)\n", 
                    status, playerNames[strategyIdx], scores[strategyIdx]);
        }
    }
}
class Nema_Aarushi_Player extends Player {
    // Constants for action choices
    private static final int COOPERATE = 0;
    private static final int DEFECT = 1;
    
    // Core strategy parameters - SIMPLIFIED approach
    private static final int BETRAYAL_THRESHOLD = 10;     // Match threshold of top performer
    private static final int ENDGAME_THRESHOLD = 95;      // Very late endgame (only last ~15 rounds)
    
    // Tracking variables
    private int totalDefectionsObserved = 0;
    private boolean inRetaliationMode = false;
    private int consecutiveCooperationCount = 0;
    
    /**
     * Selects the next action based on game history and opponent behavior patterns.
     * Simplified to focus on clear, deterministic rules that mirror top performers.
     */
    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        // First round always cooperate
        if (n == 0) return COOPERATE;
        
        // Update our tracking variables
        updateStats(n, oppHistory1, oppHistory2);
        
        // Very late endgame strategy (simpler)
        if (n >= ENDGAME_THRESHOLD) {
            return endgameStrategy(n);
        }
        
        // Main strategy logic - based on top performers
        
        // If in retaliation mode, check if we can exit based on consecutive cooperation
        if (inRetaliationMode) {
            // Only exit retaliation mode if BOTH opponents cooperated for 3 consecutive rounds
            if (consecutiveCooperationCount >= 3) {
                inRetaliationMode = false;
                return COOPERATE;
            }
            return DEFECT;
        }
        
        // If both opponents defected in the last round, immediately defect
        if (oppHistory1[n-1] == DEFECT && oppHistory2[n-1] == DEFECT) {
            return DEFECT;
        }
        
        // If total defections exceed threshold, enter retaliation mode
        if (totalDefectionsObserved >= BETRAYAL_THRESHOLD) {
            inRetaliationMode = true;
            return DEFECT;
        }
        
        // UnforgivingPlayer-inspired response to single defector
        // If either opponent defected, retaliate specifically against consistent defection
        if (oppHistory1[n-1] == DEFECT || oppHistory2[n-1] == DEFECT) {
            // Check if this opponent is a consistent defector in recent history
            if (isConsistentDefector(oppHistory1, n) || isConsistentDefector(oppHistory2, n)) {
                return DEFECT;
            }
        }
        
        // Default to cooperation
        return COOPERATE;
    }
    
    /**
     * Updates statistics based on opponent actions.
     */
    private void updateStats(int n, int[] oppHistory1, int[] oppHistory2) {
        // Track defections observed in this round
        boolean defectionThisRound = false;
        
        if (oppHistory1[n-1] == DEFECT || oppHistory2[n-1] == DEFECT) {
            totalDefectionsObserved++;
            defectionThisRound = true;
            consecutiveCooperationCount = 0; // Reset consecutive cooperation counter
        }
        
        // If both opponents cooperated, increment consecutive cooperation count
        if (oppHistory1[n-1] == COOPERATE && oppHistory2[n-1] == COOPERATE) {
            consecutiveCooperationCount++;
        } else {
            consecutiveCooperationCount = 0;
        }
    }
    
    /**
     * Checks if an opponent has been consistently defecting recently.
     * Simple deterministic check without probability.
     */
    private boolean isConsistentDefector(int[] oppHistory, int n) {
        // Need at least 3 rounds of history
        if (n < 3) return false;
        
        // Count defections in last 3 rounds
        int recentDefections = 0;
        for (int i = Math.max(0, n-3); i < n; i++) {
            if (oppHistory[i] == DEFECT) {
                recentDefections++;
            }
        }
        
        // If more than half of recent moves were defections, consider them a consistent defector
        return recentDefections >= 2;
    }
    
    /**
     * Simple, deterministic endgame strategy.
     * Based on clear rules rather than probabilistic decisions.
     */
    private int endgameStrategy(int n) {
        int remainingRounds = 110 - n; // Assuming ~110 rounds total
        
        // Very simple endgame: 
        // - Always defect in final 5 rounds
        // - For rounds 6-15 from the end, defect every other round
        if (remainingRounds <= 5) {
            return DEFECT;
        } else if (remainingRounds <= 15) {
            return (remainingRounds % 2 == 0) ? DEFECT : COOPERATE;
        }
        
        // Otherwise, maintain regular strategy
        return COOPERATE;
    }
}
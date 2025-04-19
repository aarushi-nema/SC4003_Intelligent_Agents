public class OptimizeStrategy {
	
	/* 
	 This Java program models the two-player Prisoner's Dilemma game.
	 We use the integer "0" to represent cooperation, and "1" to represent 
	 defection. 
	 
	 Recall that in the 2-players dilemma, U(DC) > U(CC) > U(DD) > U(CD), where
	 we give the payoff for the first player in the list. We want the three-player game 
	 to resemble the 2-player game whenever one player's response is fixed, and we
	 also want symmetry, so U(CCD) = U(CDC) etc. This gives the unique ordering
	 
	 U(DCC) > U(CCC) > U(DDC) > U(CDC) > U(DDD) > U(CDD)
	 
	 The payoffs for player 1 are given by the following matrix: */
	
	static int[][][] payoff = {  
		{{6,3},  //payoffs when first and second players cooperate 
		 {3,0}}, //payoffs when first player coops, second defects
		{{8,5},  //payoffs when first player defects, second coops
	     {5,2}}};//payoffs when first and second players defect
	
	/* 
	 So payoff[i][j][k] represents the payoff to player 1 when the first
	 player's action is i, the second player's action is j, and the
	 third player's action is k.
	 
	 In this simulation, triples of players will play each other repeatedly in a
	 'match'. A match consists of about 100 rounds, and your score from that match
	 is the average of the payoffs from each round of that match. For each round, your
	 strategy is given a list of the previous plays (so you can remember what your 
	 opponent did) and must compute the next action.  */
	
	
	abstract class Player {
		// This procedure takes in the number of rounds elapsed so far (n), and 
		// the previous plays in the match, and returns the appropriate action.
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			throw new RuntimeException("You need to override the selectAction method.");
		}
		
		// Used to extract the name of this player class.
		final String name() {
			String result = getClass().getName();
			return result.substring(result.indexOf('$')+1);
		}
	}
	
	/* Here are four simple strategies: */
	
	class NicePlayer extends Player {
		//NicePlayer always cooperates
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 0; 
		}
	}
	
	class NastyPlayer extends Player {
		//NastyPlayer always defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 1; 
		}
	}
	
	class RandomPlayer extends Player {
		//RandomPlayer randomly picks his action each time
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (Math.random() < 0.5)
				return 0;  //cooperates half the time
			else
				return 1;  //defects half the time
		}
	}
	
	class TolerantPlayer extends Player {
		//TolerantPlayer looks at his opponents' histories, and only defects
		//if at least half of the other players' actions have been defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			int opponentCoop = 0;
			int opponentDefect = 0;
			for (int i=0; i<n; i++) {
				if (oppHistory1[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			for (int i=0; i<n; i++) {
				if (oppHistory2[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			if (opponentDefect > opponentCoop)
				return 1;
			else
				return 0;
		}
	}
	
	class FreakyPlayer extends Player {
		//FreakyPlayer determines, at the start of the match, 
		//either to always be nice or always be nasty. 
		//Note that this class has a non-trivial constructor.
		int action;
		FreakyPlayer() {
			if (Math.random() < 0.5)
				action = 0;  //cooperates half the time
			else
				action = 1;  //defects half the time
		}
		
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return action;
		}	
	}

	class T4TPlayer extends Player {
		//Picks a random opponent at each play, 
		//and uses the 'tit-for-tat' strategy against them 
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n==0) return 0; //cooperate by default
			if (Math.random() < 0.5)
				return oppHistory1[n-1];
			else
				return oppHistory2[n-1];
		}	
	}

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

    /* IMPLEMENTING NEW PLAYERS FROM THE REPORT */
    class DistrustfulMimicPlayer extends Player {
        // Begins with defection and then copies opponent's previous moves
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // In first round, show distrust by defecting
            if(n == 0) return 1;
            // If either opponent defected last round, also defect
            if(oppHistory1[n-1] == 1 || oppHistory2[n-1] == 1) return 1;
            // Otherwise cooperate
            return 0;
        }
    }
    
    class PatternSwitchPlayer extends Player {
        // Follows a fixed pattern regardless of opponent behavior
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // Switch between cooperation and defection based on round number
            return n % 2;
        }
    }
    
    class ThresholdTolerancePlayer extends Player {
        // Cooperates until opponent defections exceed a threshold
        int maxBetrayal = 10;
        
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // Always cooperate in the first round
            if(n == 0) return 0;
            
            // Count total defections from both opponents
            int defectionCount = 0;
            for(int i = 0; i < oppHistory1.length; i++) {
                if(oppHistory1[i] == 1 || oppHistory2[i] == 1) defectionCount++;
            }
            
            // Cooperate if under threshold, otherwise defect
            return (defectionCount < maxBetrayal) ? 0 : 1;
        }
    }
    
    class UnforgivingPlayer extends Player {
        // Never forgives a single defection
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // Start with cooperation
            if(n == 0) return 0;
            
            // Search history for any defection
            for(int i = 0; i < oppHistory1.length; i++) {
                // If any defection is found, permanently defect
                if(oppHistory1[i] == 1 || oppHistory2[i] == 1) return 1;
            }
            
            // No defections found, continue cooperating
            return 0;
        }
    }
    
    class ConsensusBasedPlayer extends Player {
        // Strategy based on whether all players made the same choice
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // First round strategy is cooperation
            if(n == 0) return 0;
            
            // If all three players made the same choice in previous round, cooperate
            if(oppHistory1[n-1] == myHistory[n-1] && oppHistory2[n-1] == myHistory[n-1]) return 0;
            
            // If there was disagreement, defect
            return 1;
        }
    }
    
    class FiniteCooperationPlayer extends Player {
        // Has a limited budget of cooperation moves
        int cooperationBudget = 40;
        
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // Begin with cooperation
            if(n == 0) return 0;
            
            // Count how many times we've cooperated
            int cooperationCount = 0;
            for(int i = 0; i < myHistory.length; i++) {
                if(myHistory[i] == 0) cooperationCount++;
            }
            
            // Only cooperate if both opponents cooperated last round
            // and we haven't exceeded our cooperation budget
            if(oppHistory1[n-1] == 0 && oppHistory2[n-1] == 0 && cooperationCount < cooperationBudget) {
                return 0;
            } else {
                return 1;
            }
        }
    }
    
    class ReconciliationPlayer extends Player {
        // Will return to cooperation if opponents demonstrate trustworthiness
        boolean trustBroken = false;
        
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // Start with cooperation
            if(n == 0) return 0;
            
            if(!trustBroken) {
                // If trust hasn't been broken, check if opponents cooperated
                if(oppHistory1[n-1] == 0 && oppHistory2[n-1] == 0) {
                    // Both opponents cooperated, maintain cooperation
                    return 0;
                } else {
                    // At least one opponent defected, break trust
                    trustBroken = true;
                    return 1;
                }
            } else {
                // Trust was previously broken, check if it can be restored
                if(bothOpponentsShowedLoyalty(n, oppHistory1) && bothOpponentsShowedLoyalty(n, oppHistory2)) {
                    // Trust can be restored if both opponents cooperated twice in a row
                    trustBroken = false;
                    return 0;
                } else {
                    // Continue defecting until trust is restored
                    return 1;
                }
            }
        }
        
        // Helper method to check if an opponent has cooperated in the last two rounds
        boolean bothOpponentsShowedLoyalty(int n, int[] oppHistory) {
            return (n >= 2 && oppHistory[n-1] == 0 && oppHistory[n-2] == 0);
        }
    }
    
    
    class ConditionalReconciliationPlayer extends Player {
        // Can restore trust but has a limit to total betrayals
        boolean trustBroken = false;
        int betrayalLimit = 10;
        
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // First round always cooperate
            if(n == 0) return 0;
            
            // Check if total betrayals exceed limit
            if(betrayalLimitExceeded(n, oppHistory1, oppHistory2)) {
                trustBroken = true;
                return 1;
            }
            
            if(!trustBroken) {
                // If trust is intact, check if opponents are cooperating
                if(oppHistory1[n-1] == 0 && oppHistory2[n-1] == 0) {
                    // Both cooperated, maintain cooperation
                    return 0;
                } else {
                    // One or both defected, break trust
                    trustBroken = true;
                    return 1;
                }
            } else {
                // Trust is broken, check if reconciliation is possible
                if(bothOpponentsShowedLoyalty(n, oppHistory1) && bothOpponentsShowedLoyalty(n, oppHistory2)) {
                    // Restore trust if both cooperated twice consecutively
                    trustBroken = false;
                    return 0;
                } else {
                    // Continue defecting
                    return 1;
                }
            }
        }
        
        boolean betrayalLimitExceeded(int n, int[] oppHistory1, int[] oppHistory2) {
            // Count total defections from both opponents
            int betrayals = 0;
            for(int i = 0; i < oppHistory1.length; i++) {
                if(oppHistory1[i] == 1 || oppHistory2[i] == 1) betrayals++;
            }
            return (betrayals > betrayalLimit);
        }
        
        boolean bothOpponentsShowedLoyalty(int n, int[] oppHistory) {
            return (n >= 2 && oppHistory[n-1] == 0 && oppHistory[n-2] == 0);
        }
    }

    class PeacemakerPlayer extends Player {
    // Defects in response to defection but tries to restore cooperation
    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        // Start with cooperation
        if(n == 0) return 0;
        
        // If we defected last round, cooperate to restore peace
        if(myHistory[n - 1] == 1) return 0;
        
        // If either opponent defected, respond with defection
        if(oppHistory1[n - 1] == 1 || oppHistory2[n - 1] == 1) return 1;
        
        // Otherwise, continue cooperation
        return 0;
    }
}
    /* END OF CUSTOM CLASSES */

	
	/* In our tournament, each pair of strategies will play one match against each other. 
	 This procedure simulates a single match and returns the scores. */
	float[] scoresOfMatch(Player A, Player B, Player C, int rounds) {
		int[] HistoryA = new int[0], HistoryB = new int[0], HistoryC = new int[0];
		float ScoreA = 0, ScoreB = 0, ScoreC = 0;
		
		for (int i=0; i<rounds; i++) {
			int PlayA = A.selectAction(i, HistoryA, HistoryB, HistoryC);
			int PlayB = B.selectAction(i, HistoryB, HistoryC, HistoryA);
			int PlayC = C.selectAction(i, HistoryC, HistoryA, HistoryB);
			ScoreA = ScoreA + payoff[PlayA][PlayB][PlayC];
			ScoreB = ScoreB + payoff[PlayB][PlayC][PlayA];
			ScoreC = ScoreC + payoff[PlayC][PlayA][PlayB];
			HistoryA = extendIntArray(HistoryA, PlayA);
			HistoryB = extendIntArray(HistoryB, PlayB);
			HistoryC = extendIntArray(HistoryC, PlayC);
		}
		float[] result = {ScoreA/rounds, ScoreB/rounds, ScoreC/rounds};
		return result;
	}
	
//	This is a helper function needed by scoresOfMatch.
	int[] extendIntArray(int[] arr, int next) {
		int[] result = new int[arr.length+1];
		for (int i=0; i<arr.length; i++) {
			result[i] = arr[i];
		}
		result[result.length-1] = next;
		return result;
	}
	
	/* The procedure makePlayer is used to reset each of the Players 
	 (strategies) in between matches. When you add your own strategy,
	 you will need to add a new entry to makePlayer, and change numPlayers.*/
	
     int numPlayers = 16;
     Player makePlayer(int which) {
         switch (which) {
         case 0: return new NicePlayer();
         case 1: return new NastyPlayer();
         case 2: return new RandomPlayer();
         case 3: return new TolerantPlayer();
         case 4: return new FreakyPlayer();
         case 5: return new T4TPlayer();
         case 6: return new Nema_Aarushi_Player();
         case 7: return new DistrustfulMimicPlayer();     // Renamed from SuspiciousT4TPlayer
         case 8: return new PatternSwitchPlayer();        // Renamed from AlternatePlayer
         case 9: return new ThresholdTolerancePlayer();   // Renamed from LimitedForgivenessPlayer
         case 10: return new UnforgivingPlayer();         // Renamed from GrimTriggerPlayer
         case 11: return new ConsensusBasedPlayer();      // Renamed from WinStayLoseShiftPlayer
         case 12: return new FiniteCooperationPlayer();   // Renamed from IncreasingGreedPlayer
         case 13: return new ReconciliationPlayer();      // Renamed from ReversibleTriggerPlayer
         case 14: return new ConditionalReconciliationPlayer(); // Renamed from LimitedReversibleTriggerPlayer
         case 15: return new PeacemakerPlayer();          // Renamed from CooperativeT4TPlayer
         }
         throw new RuntimeException("Bad argument passed to makePlayer");
     
	}
}
public class ThreePrisonersDilemma {
	
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
        
        // Strategy parameters
        private static final float INITIAL_TRUST = 0.5f;
        private static final float TRUST_INCREMENT = 0.1f;
        private static final float TRUST_DECREMENT = 0.2f;
        private static final float HIGH_TRUST_THRESHOLD = 0.7f;
        private static final float LOW_TRUST_THRESHOLD = 0.3f;
        private static final int FORGIVENESS_INTERVAL = 7;
        private static final int ENDGAME_THRESHOLD = 90;
        
        // Trust scores for each opponent
        private float trustScore1 = INITIAL_TRUST;
        private float trustScore2 = INITIAL_TRUST;
        
        // Cooperation statistics
        private int myCoopCount = 0;
        private int opp1CoopCount = 0;
        private int opp2CoopCount = 0;
        
        /**
         * Selects the next action based on game history and opponent behavior patterns.
         * 
         * @param n Round number (0-indexed)
         * @param myHistory My past actions
         * @param oppHistory1 First opponent's past actions
         * @param oppHistory2 Second opponent's past actions
         * @return Action to take (0 for cooperate, 1 for defect)
         */
        int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // First round strategy: cooperate to establish potential for cooperation
            if (n == 0) {
                return COOPERATE;
            }
            
            // Update trust scores and statistics based on previous round
            updateTrustAndStats(n, myHistory, oppHistory1, oppHistory2);
            
            // Calculate cooperation rates
            float myCoopRate = (float) myCoopCount / n;
            float opp1CoopRate = (float) opp1CoopCount / n;
            float opp2CoopRate = (float) opp2CoopCount / n;
            
            // Check if we're in endgame (last ~10 rounds)
            if (n > ENDGAME_THRESHOLD) {
                return endgameStrategy(n, myHistory, oppHistory1, oppHistory2, opp1CoopRate, opp2CoopRate);
            }
            
            // Check if both opponents have been consistently cooperative
            boolean bothOpponentsCooperative = areBothOpponentsCooperative(n, oppHistory1, oppHistory2);
            
            // Check if we're being exploited (both opponents defecting while we cooperate)
            boolean beingExploited = myHistory[n-1] == COOPERATE && 
                                    oppHistory1[n-1] == DEFECT && 
                                    oppHistory2[n-1] == DEFECT;
            
            // Check if we should test cooperation (forgiveness)
            boolean shouldTestCooperation = n % FORGIVENESS_INTERVAL == 0 && 
                                        (trustScore1 > LOW_TRUST_THRESHOLD || trustScore2 > LOW_TRUST_THRESHOLD);
            
            // Decision logic
            if (bothOpponentsCooperative && trustScore1 > HIGH_TRUST_THRESHOLD && trustScore2 > HIGH_TRUST_THRESHOLD) {
                // Cooperate when both opponents are trustworthy and cooperative
                return COOPERATE;
            } else if (beingExploited) {
                // Defect if we were just exploited
                return DEFECT;
            } else if (shouldTestCooperation) {
                // Occasionally test cooperation to explore opportunities
                return COOPERATE;
            } else if (trustScore1 < LOW_TRUST_THRESHOLD && trustScore2 < LOW_TRUST_THRESHOLD) {
                // Default to defection when trust is low
                return DEFECT;
            } else if (recentTrend(oppHistory1, n) && recentTrend(oppHistory2, n)) {
                // If both opponents are trending toward cooperation, reciprocate
                return COOPERATE;
            } else {
                // Default strategy: defect
                return DEFECT;
            }
        }
        
        /**
         * Updates trust scores and cooperation statistics based on the previous round.
         */
        private void updateTrustAndStats(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
            // Skip if this is the first round
            if (n <= 0) return;
            
            // Update cooperation counts
            if (myHistory[n-1] == COOPERATE) myCoopCount++;
            if (oppHistory1[n-1] == COOPERATE) opp1CoopCount++;
            if (oppHistory2[n-1] == COOPERATE) opp2CoopCount++;
            
            // Update trust scores based on opponents' actions
            if (oppHistory1[n-1] == COOPERATE) {
                trustScore1 = Math.min(1.0f, trustScore1 + TRUST_INCREMENT);
            } else {
                trustScore1 = Math.max(0.0f, trustScore1 - TRUST_DECREMENT);
            }
            
            if (oppHistory2[n-1] == COOPERATE) {
                trustScore2 = Math.min(1.0f, trustScore2 + TRUST_INCREMENT);
            } else {
                trustScore2 = Math.max(0.0f, trustScore2 - TRUST_DECREMENT);
            }
        }
        
        /**
         * Determines if both opponents have been consistently cooperative recently.
         */
        private boolean areBothOpponentsCooperative(int n, int[] oppHistory1, int[] oppHistory2) {
            // Need at least a few rounds to determine cooperation pattern
            if (n < 3) return false;
            
            // Check last 3 rounds
            int cooperativeRounds1 = 0;
            int cooperativeRounds2 = 0;
            
            for (int i = 1; i <= Math.min(3, n); i++) {
                if (oppHistory1[n-i] == COOPERATE) cooperativeRounds1++;
                if (oppHistory2[n-i] == COOPERATE) cooperativeRounds2++;
            }
            
            return cooperativeRounds1 >= 2 && cooperativeRounds2 >= 2;
        }
        
        /**
         * Detects if an opponent is trending toward cooperation in recent rounds.
         */
        private boolean recentTrend(int[] oppHistory, int n) {
            int lookback = Math.min(5, n);
            if (lookback < 3) return false;
            
            int recentCoopCount = 0;
            for (int i = 0; i < lookback; i++) {
                if (oppHistory[n-1-i] == COOPERATE) {
                    recentCoopCount++;
                }
            }
            
            return (float)recentCoopCount / lookback > 0.6f;
        }
        
        /**
         * Special strategy for the endgame phase.
         */
        private int endgameStrategy(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2, 
                                float opp1CoopRate, float opp2CoopRate) {
            // If both opponents have been highly cooperative, consider defecting for maximum points
            if (opp1CoopRate > 0.8 && opp2CoopRate > 0.8) {
                // Check if they're likely to continue cooperating even if we defect
                boolean opp1Tolerant = detectTolerance(myHistory, oppHistory1, n);
                boolean opp2Tolerant = detectTolerance(myHistory, oppHistory2, n);
                
                if (opp1Tolerant && opp2Tolerant) {
                    return DEFECT; // Exploit tolerant opponents in endgame
                }
            }
            
            // If one opponent is consistently defecting, match their behavior
            if (opp1CoopRate < 0.2) {
                return DEFECT;
            }
            
            if (opp2CoopRate < 0.2) {
                return DEFECT;
            }
            
            // If we've established mutual cooperation, maintain it unless very close to the end
            if (opp1CoopRate > 0.7 && opp2CoopRate > 0.7 && n < 95) {
                return COOPERATE;
            }
            
            // Default endgame strategy: defect
            return DEFECT;
        }
        
        /**
         * Attempt to detect if an opponent is tolerant (continues to cooperate despite defections).
         */
        private boolean detectTolerance(int[] myHistory, int[] oppHistory, int n) {
            int defectionCount = 0;
            int cooperationAfterDefect = 0;
            
            for (int i = 0; i < n-1; i++) {
                if (myHistory[i] == DEFECT) {
                    defectionCount++;
                    if (oppHistory[i+1] == COOPERATE) {
                        cooperationAfterDefect++;
                    }
                }
            }
            
            return defectionCount > 0 && (float)cooperationAfterDefect / defectionCount > 0.5f;
        }
    }

    /* END OF CUSTOM CLASS */

	
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
	
	int numPlayers = 7;
	Player makePlayer(int which) {
		switch (which) {
		case 0: return new NicePlayer();
		case 1: return new NastyPlayer();
		case 2: return new RandomPlayer();
		case 3: return new TolerantPlayer();
		case 4: return new FreakyPlayer();
		case 5: return new T4TPlayer();
        case 6: return new Nema_Aarushi_Player();
		}
		throw new RuntimeException("Bad argument passed to makePlayer");
	}
	
	/* Finally, the remaining code actually runs the tournament. */
	
	public static void main (String[] args) {
		ThreePrisonersDilemma instance = new ThreePrisonersDilemma();
		instance.runTournament();
	}
	
	boolean verbose = true; // set verbose = false if you get too much text output
	
	void runTournament() {
		float[] totalScore = new float[numPlayers];

		// This loop plays each triple of players against each other.
		// Note that we include duplicates: two copies of your strategy will play once
		// against each other strategy, and three copies of your strategy will play once.

		for (int i=0; i<numPlayers; i++) for (int j=i; j<numPlayers; j++) for (int k=j; k<numPlayers; k++) {

			Player A = makePlayer(i); // Create a fresh copy of each player
			Player B = makePlayer(j);
			Player C = makePlayer(k);
			int rounds = 90 + (int)Math.rint(20 * Math.random()); // Between 90 and 110 rounds
			float[] matchResults = scoresOfMatch(A, B, C, rounds); // Run match
			totalScore[i] = totalScore[i] + matchResults[0];
			totalScore[j] = totalScore[j] + matchResults[1];
			totalScore[k] = totalScore[k] + matchResults[2];
			if (verbose)
				System.out.println(A.name() + " scored " + matchResults[0] +
						" points, " + B.name() + " scored " + matchResults[1] + 
						" points, and " + C.name() + " scored " + matchResults[2] + " points.");
		}
		int[] sortedOrder = new int[numPlayers];
		// This loop sorts the players by their score.
		for (int i=0; i<numPlayers; i++) {
			int j=i-1;
			for (; j>=0; j--) {
				if (totalScore[i] > totalScore[sortedOrder[j]]) 
					sortedOrder[j+1] = sortedOrder[j];
				else break;
			}
			sortedOrder[j+1] = i;
		}
		
		// Finally, print out the sorted results.
		if (verbose) System.out.println();
		System.out.println("Tournament Results");
		for (int i=0; i<numPlayers; i++) 
			System.out.println(makePlayer(sortedOrder[i]).name() + ": " 
				+ totalScore[sortedOrder[i]] + " points.");
		
	} // end of runTournament()
	
} // end of class PrisonersDilemma

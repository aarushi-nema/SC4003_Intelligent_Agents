import java.util.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;


public class GameTheoryAnalyzer {

    static int[][][] payoff = OptimizeStrategy.payoff;

    public static void analyze() {
        System.out.println("\n========================================");
        System.out.println("        GAME THEORY ANALYSIS REPORT      ");
        System.out.println("========================================");

        List<int[]> allProfiles = generateAllActionProfiles();

        System.out.println("\nNash Equilibria Found:");
        boolean foundNash = false;
        for (int[] profile : allProfiles) {
            if (isNashEquilibrium(profile)) {
                System.out.printf("- Strategy %s is a Nash Equilibrium\n", Arrays.toString(profile));
                foundNash = true;
            }
        }
        if (!foundNash) System.out.println("  (None found)");

        System.out.println("\nPareto Optimal Profiles:");
        boolean foundPareto = false;
        for (int[] profile : allProfiles) {
            if (isParetoOptimal(profile)) {
                System.out.printf("- Strategy %s is Pareto Optimal\n", Arrays.toString(profile));
                foundPareto = true;
            }
        }
        if (!foundPareto) System.out.println("  (None found)");

        System.out.println("\nDominant Strategy Analysis:");
        for (int player = 0; player < 3; player++) {
            String result = checkDominantStrategy(player);
            System.out.printf("- Player %d: %s\n", (player+1), result);
        }
        System.out.println("========================================\n");
    }

    static List<int[]> generateAllActionProfiles() {
        List<int[]> profiles = new ArrayList<>();
        for (int a = 0; a <= 1; a++)
            for (int b = 0; b <= 1; b++)
                for (int c = 0; c <= 1; c++)
                    profiles.add(new int[]{a, b, c});
        return profiles;
    }

    static boolean isNashEquilibrium(int[] profile) {
        int[] originalPayoffs = getPayoffs(profile);

        for (int i = 0; i < 3; i++) {
            int originalAction = profile[i];
            int flippedAction = 1 - originalAction;

            int[] newProfile = profile.clone();
            newProfile[i] = flippedAction;
            int[] newPayoffs = getPayoffs(newProfile);

            if (newPayoffs[i] > originalPayoffs[i]) {
                return false; // unilateral improvement found
            }
        }
        return true;
    }

    static boolean isParetoOptimal(int[] profile) {
        int[] basePayoff = getPayoffs(profile);
        for (int[] altProfile : generateAllActionProfiles()) {
            if (Arrays.equals(profile, altProfile)) continue;
            int[] altPayoff = getPayoffs(altProfile);

            boolean atLeastOneBetter = false;
            boolean noneWorse = true;

            for (int i = 0; i < 3; i++) {
                if (altPayoff[i] > basePayoff[i]) atLeastOneBetter = true;
                if (altPayoff[i] < basePayoff[i]) noneWorse = false;
            }

            if (atLeastOneBetter && noneWorse) return false;
        }
        return true;
    }

    static String checkDominantStrategy(int player) {
        boolean action0AlwaysBetter = true;
        boolean action1AlwaysBetter = true;

        for (int b = 0; b <= 1; b++) {
            for (int c = 0; c <= 1; c++) {
                int[] prof0 = new int[]{0, b, c};
                int[] prof1 = new int[]{1, b, c};

                int payoff0 = getPayoffs(switchIndex(prof0, player))[player];
                int payoff1 = getPayoffs(switchIndex(prof1, player))[player];

                if (payoff0 < payoff1) action0AlwaysBetter = false;
                if (payoff1 < payoff0) action1AlwaysBetter = false;
            }
        }

        if (action0AlwaysBetter) return "Dominant Strategy = Cooperate (0)";
        if (action1AlwaysBetter) return "Dominant Strategy = Defect (1)";
        return "No dominant strategy";
    }

    static int[] switchIndex(int[] profile, int playerIndex) {
        int[] ordered = new int[3];
        for (int i = 0; i < 3; i++)
            ordered[i] = profile[(i + playerIndex) % 3];
        return ordered;
    }

    static int[] getPayoffs(int[] profile) {
        return new int[]{
            payoff[profile[0]][profile[1]][profile[2]],
            payoff[profile[1]][profile[2]][profile[0]],
            payoff[profile[2]][profile[0]][profile[1]]
        };
    }
}

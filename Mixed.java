//Tibor Mester, CMSCM 474 ID:117977318
//using algorithm outlined in: http://mason.gmu.edu/~kliu3/personal/Selected_Projects_files/LemkeHowson.pdf
import java.util.Scanner;
import java.util.Arrays;

public class Mixed {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Read the size of the payoff matrices
        int n = scanner.nextInt();

        // Read the payoff matrices for both players
        Double[][] player1Payoffs = new Double[n][n];
        Double[][] player2Payoffs = new Double[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                player1Payoffs[i][j] = scanner.nextDouble();
            }
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                player2Payoffs[j][i] = scanner.nextDouble();
            }
        }

        // Find the Nash equilibrium in one of two ways
        double[][] strategies = equilibrium(player1Payoffs, player2Payoffs);

        // Print the Nash equilibrium strategies
        for (int i = 0; i < n; i++) {
            System.out.printf("%.4f ", strategies[0][i]);
        }
        System.out.println();

        for (int i = 0; i < n; i++) {
            System.out.printf("%.4f ", strategies[1][i]);
        }
        System.out.println();

        scanner.close();
    }

    // Implement the algorithm to find mixed Nash equilibrium
    private static double[][] equilibrium(Double[][] A, Double[][] B) {
        int n = A.length;
        double[][] strategies = new double[2][n];

        // check for a pure strategy in O(n^2)
        for (int i = 0; i < n; i++) { // let i in set of n
            // iterate through the rows
            double bestInRow = -101;
            double bestInColumn = -101;
            int bestIndex = -1;
            for (int j = 0; j < n; j++) { // let j in set of m
                // iterate through the columns in row i to find the best one
                if (A[i][j] > bestInRow) {
                    bestInRow = A[i][j];
                    bestInColumn = B[j][i]; // has to be transposed...
                    bestIndex = j; //index of the column that has the best from A
                }
            }
            for (int j = 0; j < n; j++) {
                // iterate through the column for playerB to see if this is the best one
                if (B[bestIndex][j] > bestInColumn) {
                    bestInColumn = 101; // past allowed values
                }
            }
            if (bestInColumn < 101) {
                Arrays.fill(strategies[0], 0.0);
                strategies[0][bestIndex] = 1;
                Arrays.fill(strategies[1], 0.0);
                strategies[1][i] = 1;
                return strategies;
            }
        }
        // otherwise we need to check for mixed strategies....
        //Preproccessing... Add 100 to each element to ensure >0
        for (int i = 0; i < n; i++){
            for (int j = 0; j < n; j++){
                A[i][j] += 100.0;
                B[i][j] += 100.0;
            }
        }
        /*Data: LemkeHowson(U1, U2) Result: p, q
        (m,n)=size(U1 );
        P =[U2T,I,1];
        Q = [I,U1,1]; LP=[1,...,m]; LQ=[m+1,...,m+n]; k=k0;
        */
        Double[][] P  = new Double[n][2*n + 1];
        Double[][] Q  = new Double[n][2*n + 1];
        for (int i = 0; i < n; i++){
            for (int j = 0; j < n; j++){
                if (i == j){
                    Q[i][j] = 1.0;
                } else {
                    Q[i][j] = 0.0;
                }
                P[i][j] = B[j][i];
                
            }
        }
        for (int i = 0; i < n; i++){
            for (int j = n; j < 2*n; j++){
                if (i == (j - n)){
                    P[i][j] = 1.0;
                } else {
                    P[i][j] = 0.0;
                }
                Q[i][j] = A[i][j-n];
            }
        }
        int[] LP = new int[2*n];
        int[] LQ = new int[2*n];
        Arrays.fill(LP, 0);
        Arrays.fill(LQ, 0);
        for (int i = 0; i < n; i++){
            P[i][2*n] = 1.0;
            Q[i][2*n] = 1.0;
            LP[i] = 1;
            LQ[n+i] = 1;
        }
        int k0 = 0;
        int k = k0;
        /*
        while 1 do 
            Remove(LP,k);
            [P, k]=Pivot(P, k); 
            Add(LP,k);
            if k=k0 then
                break;
            end
            Remove(LQ,k);
            [Q, k]=Pivot(Q, k); Add(LQ,k);
            if k=k0 then
                break;
        end end
        */
        Object[] results = new Object[2];
        while (true){   
            results = pivot(P, k, LP);
            LP[k] = 0; //remove old k
            P = (Double[][])results[0];
            k = (int)results[1]; 
            LP[k] = 1; //add new k
            if (k == k0){
                break;
            }
            results = pivot(Q, k, LQ);
            LQ[k] = 0;
            Q = (Double[][])results[0];
            k = (int)results[1];
            LQ[k] = 1;
            if (k == k0){
                break;
            }
        }
        /**
         * [p,q]=CalculateWithLabel(P,Q,LP,LQ); return normal(p), normal(q);
         */
        strategies = CalculateWithLabel(P, Q, LP, LQ);

        return strategies;
    }
    /**Data: 
     * pivot(M, k0, cl) Result: M, k, cl (m,n)=size(M);
        k=k0;
        max=0;
        for i ← 1 to m do
            t = Mi,k0/Mi,n; if t > max then
            ind=i;
        end 
        end
        if max > 0 then 
            swap(k, cl(ind)); 
            for i ← 1 to m do
                if i=ind then 
                    continue;
                end
                for j ← 1 to n do
                    Mi,j = Mi,j − (Mi,k0/Mind,k0)Mk,j; end
                end 
            end
        return M, k; */
    private static Object[] pivot(Double[][] M, int l, int[] LM){
        Object[] results = new Object[2];
        int k = l;
        double max = 0.0;
        double t;
        int n = M.length;
        int ind = -1;
        for (int i = 0; i < n; i++){
            t = M[i][k] / M[i][2*n];
            if( t > max){
                max = t;
                ind = i;
            }
        }
        if (max > 0.0){
            //idk what it means by complement tbh, i think it is as follows
            //ind is what row is the complementary label
            //complementary labels are ordered 0,1,...2n-1, skipping when LM[i] == 1
            //cl(ind) returns the label value of the index
            int skips = 0;
            for (int i = 0; i <= ind; i++){
                //gets the ind-th label that isn't abt to be removed nor in M
                while(LM[i+skips] == 1){
                    skips++;
                }
            }
            int cl = skips + ind;
            k = cl;
            //swap(k, complement(ind))
            for (int i = 0; i < n; i++){
                if (i == ind){
                    continue;
                }
                double scale = M[i][l] / M[ind][l];
                for (int j = 0; j < (2 * n) + 1; j++) {
                    M[i][j] -= scale * M[ind][j];
                }
            }

        }

        results[0] = M;
        results[1] = k;
        return results;
    }

    // Define a method to calculate mixed strategies using labels
    private static double[][] CalculateWithLabel(
            Double[][] P, Double[][] Q, int[] LP, int[] LQ) {

        int n = P.length;

        // Initialize the mixed strategies for both players
        double[] p = new double[n];
        double[] q = new double[n];

        Arrays.fill(p, 0.0);
        Arrays.fill(q, 0.0);

        // Update mixed strategies based on labels
        int pind = 0;
        int qind = 0;
        for (int i = 0; i < 2*n; i++){
            if(LP[i] == 0){
                p[pind] = P[pind][2*n] / P[pind][i];
                pind++;
            } else if(LQ[i] == 0){
                q[qind] = Q[qind][2*n] / Q[qind][i];
                qind++;
            }
        }

        // Normalize mixed strategies to ensure they sum to 1
        double pSum = 0.0;
        for (double pi : p) {
            pSum += pi;
        }

        double qSum = 0.0;
        for (double qj : q) {
            qSum += qj;
        }

        if (pSum > 0) {
            for (int i = 0; i < n; i++) {
                p[i] /= pSum;
            }
        }

        if (qSum > 0) {
            for (int j = 0; j < n; j++) {
                q[j] /= qSum;
            }
        }

        // Return the calculated mixed strategies
        return new double[][] { p, q };
    }

}
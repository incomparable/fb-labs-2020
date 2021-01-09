package aphine_app;

import java.util.ArrayList;

public class linalg {


    public static ArrayList<Integer> linsolve(int a, int b, int n){
        int d = gcd(a, n);
        int a_ = a % n;
        int a1 = a_ / d;
        int b1 = b / d;
        int n1 = n / d;
        int x0 = extendedGCD(a1, n1)[1];
        int a_1 = (b1 * x0) % n1;
        ArrayList<Integer> res = new ArrayList<Integer>();
        for (int i=0; i<d; i++ ){
            res.add(a_1 + i * n1);
        }
        ArrayList<Integer> res_ = new ArrayList<Integer>();
        for (int r: res){
            if (r < 0) {
                res_.add(r + n);
            } else {
                res_.add(r);
            }
        }
        return res_;
    }


    public static int gcd(int a,int b) {
        while (b != 0) {
            int tmp = a % b;
            a = b;
            b = tmp;
        }
        return a;
    }


    public static int[] extendedGCD(int a, int n) {
        int s1 = 1, s2 = 0;
        int t1 = 0, t2 = 1;
        while(n != 0) {
            int quotient = a / n;
            int r = a % n;
            a = n;
            n = r;
            int tempS = s1 - s2 * quotient;
            s1 = s2;
            s2 = tempS;
            int tempR = t1 - t2 * quotient;
            t1 = t2;
            t2 = tempR;
        }
        return new int[] {a, s1, t1};
    }

}

package aphine_app;

import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
		Analyzer txt = new Analyzer("doc.txt");
		String decrypted;
        ArrayList<ArrayList<Integer>> possibleSolutions = txt.solve();
        for (ArrayList<Integer> ab: possibleSolutions){
                decrypted = txt.decrypter(ab.get(0), ab.get(1));
                if (service.letterFreq(decrypted)){
                    System.out.printf("a = %d, b =  %d, text = %s\n", ab.get(0), ab.get(1), decrypted.substring(0, 30));
                }
            }
        }
    }


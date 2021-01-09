package aphine_app;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Analyzer {
    String text;
    ArrayList<String> textArray;
    LinkedHashMap<String, Integer> counted;
    LinkedHashMap<String, Integer> reducted;
    ArrayList<Integer> Xs;
    ArrayList<Integer> Ys;

    public Analyzer(String text) {

        if (text.length() < 40) {
            try {
                this.text = service.deleteOtherSymbols(service.readTextFile(text));
            } catch (IOException e) {
                System.out.println("Помилка читання файлу");
            }
        } else {
            this.text = service.deleteOtherSymbols(text);
        }


        this.textArray = new ArrayList<String>();
        for (int i=0; i < this.text.length() / 2; i++){
            this.textArray.add(this.text.substring(2*i, 2*(i+1)));
        }
        if (this.text.length() % 2 == 1){
            this.textArray.add(this.text.substring(this.text.length()-1, this.text.length()));
        }


        this.counted = new LinkedHashMap<String, Integer>();
        for (String item: this.textArray){
            if (this.counted.containsKey(item)){
                this.counted.put(item, this.counted.get(item) + 1);
            } else {
                this.counted.put(item, 1);
            }
        }


        this.counted = service.sortByValue(this.counted);
        List<String> topKeys = this.counted.keySet().stream()
                .limit(5)
                .collect(Collectors.toList());

        this.reducted = new LinkedHashMap<>();
        for (String item: topKeys){
            this.reducted.put(item, this.counted.get(item));
        }
        this.reducted = service.sortByValue(this.reducted);
    }


    public ArrayList<ArrayList<Integer>> solve(){
        ArrayList<String> rus = new ArrayList<>();
        rus.add("то"); rus.add("по"); rus.add("но"); rus.add("ст"); rus.add("на");
        rus.add("ка"); rus.add("не"); rus.add("ко"); rus.add("ал"); rus.add("ос");
        rus.add("от"); rus.add("ов"); rus.add("ро"); rus.add("ра"); rus.add("ла");
        ArrayList<String> redStr = new ArrayList<>();
        for (String item:this.reducted.keySet()){
            redStr.add(item);
        }
        this.Ys = numbers(redStr);
        this.Xs = numbers(rus);

        ArrayList<ArrayList<Integer>> XXlist = new ArrayList<ArrayList<Integer>>();
        ArrayList<ArrayList<Integer>> YYlist = new ArrayList<ArrayList<Integer>>();
        XXlist.add(Xs);
        XXlist.add(Xs);
        YYlist.add(Ys);
        YYlist.add(Ys);
        ArrayList<ArrayList<Integer>> XX = service.cartesianProduct(XXlist);
        ArrayList<ArrayList<Integer>> YY = service.cartesianProduct(YYlist);


        int m = service.alphabet.length();
        ArrayList<ArrayList<Integer>> ab_sol = new ArrayList<ArrayList<Integer>>();
        ArrayList<Integer> sol = new ArrayList<Integer>();
        for (ArrayList<Integer> xs:XX) {
            for (ArrayList<Integer> ys:YY) {
                if ((xs.get(0) != xs.get(1)) & (ys.get(0) != ys.get(1))){
                    int x_ = Math.abs(xs.get(0) - xs.get(1));
                    int y_ = Math.abs(ys.get(0) - ys.get(1));
                    ArrayList<Integer> a = linalg.linsolve(x_, y_, (int) Math.pow(m, 2));
                    for (Integer a_:a){
                        ArrayList<Integer> b = linalg.linsolve(1, ys.get(0) - a_ * xs.get(0), (int) Math.pow(m, 2));
                        for (Integer b_:b){
                            sol = new ArrayList<Integer>();
                            sol.add(a_);
                            sol.add(b_);
                            ab_sol.add(sol);
                        }
                    }
                }
            }
        }
        return ab_sol;
    }


    public String decrypter(int a, int b){
        ArrayList<String> res = new ArrayList<>();
        String result = "";
        HashMap<Integer, String> bigrams = Calc.bigrams();
        int Yi, a_, Xi;
        int m = Calc.alphabet.length();
        int m2 = (int) Math.pow(m, 2);
        a_ = linalg.linsolve(a, 1, m2).get(0);
        for (String item: this.textArray){
            Yi = Calc.bigramN(item);
            Xi = (a_ * (Yi - b)) % m2;
            if (Xi < 0){
                Xi += m2;
            }
            res.add(bigrams.get(Xi));
        }
        for (String s: res){
            result += s;
        }
        return result;
    }


    private ArrayList<Integer> numbers(ArrayList<String> bigrams){
        ArrayList<Integer> res = new ArrayList<>();
        for (String item: bigrams){
            res.add(Calc.bigramN(item));
        }
        return res;
    }
}


class Calc{
    static String alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя";

    public static Integer bigramN(String bigram){
        return alphabet.indexOf(bigram.substring(0, 1)) * alphabet.length() + alphabet.indexOf(bigram.substring(1));
    }

    public static HashMap<Integer, String> bigrams(){
        HashMap<Integer, String> res = new HashMap<>();
        for (Character l1: alphabet.toCharArray()){
            for (Character l2: alphabet.toCharArray()){
                String bigram = String.valueOf(new char []{l1, l2});
                res.put(bigramN(bigram), bigram);
            }
        }
        return res;
    }
}

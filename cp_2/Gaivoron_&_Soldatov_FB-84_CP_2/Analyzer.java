package viginer_app;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;


public class Analyzer { //клас для атаки на шифр Віженера
    String text;
    ArrayList<Character>[] splitted;
    String [] splitted_text;
    Viginer [] splitted_obj;
    Character [][] most_freq;

    public Analyzer(String text){ // констуктор класу
        if (text.length() < 40){
            try{
                this.text = viginerService.deleteOtherSymbols(viginerService.readTextFile(text));
            } catch (IOException e) {
                System.out.println("Помилка читання файлу");
            }
        } else {
            this.text = viginerService.deleteOtherSymbols(text);
        }
    }


    public float c_index_avg(int n){
        float [] indexes = new float[n];
        Viginer tmp_text;
        this.split_into(n);
        for (int i=0; i < n; i++){
            tmp_text = new Viginer(this.splitted_text[i]);
            indexes[i] = tmp_text.c_index();
        }
        return this.mean(indexes);
    }


    public void split_into_objects(){
        int n = this.splitted_text.length;
        this.splitted_obj = new Viginer[n];
        for (int i=0; i < n; i++){
            this.splitted_obj[i] = new Viginer(splitted_text[i]);
        }
    }


    public void fill_freq_rating(){
        int n = this.splitted_text.length;
        this.most_freq = new Character [n][viginerService.alphabet.length()];
        for (int i=0; i < n; i++){
            HashMap<Character, Integer> symFreq = viginerService.sortByValue(this.splitted_obj[i].countUnique());
            this.most_freq[i] = symFreq.keySet().toArray(Character[]::new);
        }
    }


    public String key_composer(int [] key_nums){
        int n = this.splitted_text.length;
        int shift;
        String abc = viginerService.alphabet;
        Character [] choose_letters = new Character[n];
        char [] key = new char[n];

        for (int i=0; i < n; i++){
            choose_letters[i] = this.most_freq[i][key_nums[i]];
        }

        for (int i=0; i < n; i++){
            shift = abc.indexOf(choose_letters[i]) - abc.indexOf('о');
            if (shift < 0) {
                shift += abc.length();
            }
            abc.getChars(shift, shift+1, key, i);
        }
        return new String(key);
    }


    public void split_into(int n){
        this.splitted = new ArrayList[n];
        for (int i=0; i < n; i++){
            this.splitted[i] = new ArrayList<Character>();
        }
        char[] char_sequence = this.text.toCharArray();
        for (int i=0; i < char_sequence.length; i++){
            this.splitted[i % n].add(char_sequence[i]);
        }

        this.splitted_text = new String[n];
        for (int i=0; i < n; i++){
            StringBuilder builder = new StringBuilder(this.splitted[i].size());
            for (Character ch: this.splitted[i]){
                builder.append(ch);
            }
            this.splitted_text[i] = builder.toString();
        }
    }


    public void show_letters(){
        int n = this.splitted_text.length;
        Character[] tmp = new Character[5];
        for (int i=0; i < n; i++){
            tmp = Arrays.copyOfRange(this.most_freq[i], 0, 5);
            System.out.printf("Підрозділ %d, букви: %s%n", i, convertLetters(tmp));
        }
    }


    private static String convertLetters(Character [] letters){
        int shift;
        int n = letters.length;
        String abc = viginerService.alphabet;
        char [] key = new char[n];
        for (int i=0; i < n; i++){
            shift = abc.indexOf(letters[i]) - abc.indexOf('о');
            if (shift < 0) {
                shift += abc.length();
            }
            abc.getChars(shift, shift+1, key, i);
        }
        return new String(key);
    }


    public double[] c_indexes(){
        Viginer item;
        int n = this.splitted_text.length;
        double [] res = new double[n];
        for (int i=0; i < n; i++){
            item = new Viginer(this.splitted_text[i]);
            res[i] = item.c_index();
        }
        return res;
    }


    private static float mean(float[] m) {
        double sum = 0;
        for (int i = 0; i < m.length; i++) {
            sum += m[i];
        }
        return (float) sum / m.length;
    }

}

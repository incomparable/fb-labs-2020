package viginer_app;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Stream;

public class Viginer {
    // клас, що відповідає за шифрування/дешифрування та оцінку параметрів тексту

    String text;

    public Viginer(String text){
        if (text.length() < 40){
            try{
                this.text = viginerService.readTextFile(text);
            } catch (IOException e) {
                System.out.println("Помилка читання файлу");
            }
        } else {
            this.text = text;
        }
    }


    public String encrypt(String key){

        char[] char_sequence = viginerService.deleteOtherSymbols(this.text).toCharArray();
        char [] key_array = key.toCharArray();
        StringBuilder res = new StringBuilder();
        HashMap<Character, Integer> d1 = viginerService.charNumbers();
        HashMap<Integer, Character> d2 = viginerService.numberedAlphabet();
        int counter = 0;
        char added_num = 0;
        Character new_symbol = new Character(' ');
        for (char symbol: char_sequence) {
            added_num = key_array[counter];
            if (d1.get(symbol) + d1.get(added_num) < viginerService.alphabet.length()) {
                new_symbol = d2.get(d1.get(symbol) + d1.get(added_num));
            } else {
                new_symbol = d2.get(d1.get(symbol) + d1.get(added_num) - viginerService.alphabet.length());
            }
            res.append(new_symbol);
            if (counter > key.length() - 2) {
                counter = 0;
            } else {
                counter += 1;
            }
        }
        return res.toString();
    }


    public String decrypt(String key){
        StringBuilder res = new StringBuilder();
        char [] key_array = key.toCharArray();
        char[] char_sequence = viginerService.deleteOtherSymbols(this.text).toCharArray();
        int counter = 0;
        char added_num = 0;
        HashMap<Character, Integer> d1 = viginerService.charNumbers();
        HashMap<Integer, Character> d2 = viginerService.numberedAlphabet();
        Character new_symbol = new Character(' ');
        for (char symbol: char_sequence) {
            added_num = key_array[counter];
            if (d1.get(symbol) - d1.get(added_num) >= 0) {
                new_symbol = d2.get(d1.get(symbol) - d1.get(added_num));
            } else {
                new_symbol = d2.get(d1.get(symbol) - d1.get(added_num) + viginerService.alphabet.length());
            }
            res.append(new_symbol);
            if (counter > key.length() - 2) {
                counter = 0;
            } else {
                counter += 1;
            }
        }
        return res.toString();
    }


    public HashMap<Character, Integer> countUnique(){
        HashMap<Character, Integer> symFreq = new HashMap<Character, Integer>();
        Stream <Character> c_sequence = new String(viginerService.deleteOtherSymbols(this.text)).chars().mapToObj(i->(char)i);
        Character [] uniques = c_sequence.distinct().toArray(Character[]::new);
        long count = 0;
        for (Character letter:uniques) {
            c_sequence = new String(viginerService.deleteOtherSymbols(this.text)).chars().mapToObj(i->(char)i);
            count = c_sequence
                    .filter(i -> i == (char)letter)
                    .count();
            symFreq.put(letter, (int) count);
        }
        return symFreq;
    }


    public float c_index(){
        HashMap<Character, Integer> c_dict = this.countUnique();
        float n = viginerService.deleteOtherSymbols(this.text).length();
        Integer [] freqs = c_dict.values().toArray(Integer[]::new);
        float sum = 0;
        for (Integer f:freqs){
            sum += (float) f*( (float) f - 1);
        }
        return 1 / (n * (n - 1)) * sum;
    }
}

class viginerService{ // клас допоміжних функцій
    public static String alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя";


    public static String readTextFile(String fileName) throws IOException {
        BufferedReader reader = new BufferedReader( new FileReader (fileName));
        String line = null;
        StringBuilder stringBuilder = new StringBuilder();
        String ls = System.getProperty("line.separator");
        while( ( line = reader.readLine() ) != null ) {
            stringBuilder.append( line );
            stringBuilder.append( ls );
        }

        stringBuilder.deleteCharAt(stringBuilder.length()-1);
        return stringBuilder.toString();
    }


    public static String deleteOtherSymbols(String text) {
        StringBuilder res = new StringBuilder();
        for (char chr : text.toLowerCase().replace("ё", "е").toCharArray()) {
            if (alphabet.indexOf(chr) > -1) {
                res.append(chr);
            }
        }
        return res.toString();
    }


    public static HashMap<Character, Integer> charNumbers(){
        HashMap<Character, Integer> res = new HashMap<Character, Integer>();
        for (int i=0; i<alphabet.length(); i++){
            res.put(alphabet.charAt(i), i);
        }
        return res;
    }


    public static HashMap<Integer, Character> numberedAlphabet(){
        HashMap<Integer, Character> res = new HashMap<Integer, Character>();
        for (int i = 0; i < alphabet.length(); i++){
            res.put(i, alphabet.charAt(i));
        }
        return res;
    }


    public static <K, V> Stream<K> keys(HashMap<K, V> map, V value) {
        return map
                .entrySet()
                .stream()
                .filter(entry -> value.equals(entry.getValue()))
                .map(HashMap.Entry::getKey);
    }


    public static <K, V extends Comparable<? super V>> HashMap<K, V>
    sortByValue(HashMap<K, V> map )
    {
        List<Map.Entry<K, V>> list =
                new LinkedList<>(map.entrySet());
        Collections.sort( list, new Comparator<Map.Entry<K, V>>()
        {
            @Override
            public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2)
            {
                return ~(o1.getValue()).compareTo( o2.getValue() );
            }
        } );

        HashMap<K, V> result = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list)
        {
            result.put(entry.getKey(), entry.getValue());
        }
        return result;
    }
}

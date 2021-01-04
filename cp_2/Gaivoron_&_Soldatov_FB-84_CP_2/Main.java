package viginer_app;

import java.util.*;
import java.util.stream.Stream;

public class Main {

    public static void main(String[] args) {
        // індекс відповідності відкритого тексту
        Viginer crypto = new Viginer("./assets/text1.txt");

        System.out.println("Розрахунок індексів відповідності");
        System.out.println("Індекс відповідності початкового тексту = " +crypto.c_index());

        // індекси відповідності зашифрованих текстів з різною довжиною ключа
        HashMap<Integer, Character> alphabet = viginerService.numberedAlphabet();
        Random rand = new Random();
        String key = "";
        Viginer crypted;
        for (int i=2; i < 21; i++){
            for (int j=0; j < i; j++){
                key += alphabet.get(rand.nextInt(alphabet.size()));
            }
            crypted = new Viginer(crypto.encrypt(key));
            System.out.print("r= " + Integer.toString(i) + " ");
            System.out.println("Індекс відповідності = " + Float.toString(crypted.c_index()));
        }

        // атака на шифр Віженера
        System.out.println("\nАтака на шифр Віжинера");
        System.out.println("Індекси відповідності для різних розбиттів тексту");
        Analyzer an_text = new Analyzer("./assets/to_decrypt.txt");
        HashMap<Integer, Float> indexes = new HashMap<Integer, Float>();
        Float tmp;
        for (int i=2; i < 21; i++) {
            tmp = an_text.c_index_avg(i);
            System.out.print("r= " + Integer.toString(i) + " ");
            System.out.println("Індекс відповідності = " + Float.toString(tmp));
            indexes.put(i, tmp);
        }
        float max_index = Collections.max(indexes.values());
        System.out.printf("Максимальний індекс = %f, ", max_index);
        Stream<Integer> keyStream1 = viginerService.keys(indexes, max_index);
        Integer proper_split = keyStream1.findFirst().get();
        System.out.printf("що відповідає %d елементів розбиття\n\n", proper_split);

        // пошук ключа
        an_text.split_into(proper_split); // розбиття тексту на визначену кількість частин
        an_text.split_into_objects(); // формування об'єктів для аналізу (службове)
        an_text.fill_freq_rating(); // визначення найбільш частих літер у кожній з частин
        String possible_key = an_text.key_composer(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
        System.out.println("Визначено наступний можливий ключ шифру: " + possible_key + "\n");
        an_text.show_letters();
        System.out.println("\nПроводимо розшифрування тексту з визначеним ключем");
        String result = new Viginer("./assets/to_decrypt.txt").decrypt(possible_key);

        // группування літер розшифрованого тексту для визначення помилок в отриманому ключі
        for (int i=0; i<10; i++){
            System.out.println(result.substring(i * possible_key.length(), (i + 1) * possible_key.length()));
        }

        // Проводимо корективи ключа
        result = new Viginer("./assets/to_decrypt.txt").decrypt("громыковедьма");
        System.out.println("Розшифрування з коректованим ключем");
        System.out.println(result);
    }
}

package com.company;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    static char[] alpha ={'а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я'};
    static String alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя";
    public static String open_text = "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\open_text.txt";
    public static String text2_cipher = "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\ключ_юг.txt";
    public static String text3_cipher= "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\ключ_лес.txt";
    public static String text4_cipher = "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\ключ_влад.txt";
    public static String text5_cipher = "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\ключ_мышка.txt";
    public static String text10_cipher = "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\ключ_клавиатура.txt";
    public static String text_cipher = "C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\open_text_3.txt";
    public static void main(String[] args) throws IOException {
       ReadFile a = new ReadFile(open_text);
       String text = a.readUsingBufferedReader(open_text);
       String text2 = a.readUsingBufferedReader(text2_cipher);
       String text3 = a.readUsingBufferedReader(text3_cipher);
       String text4 = a.readUsingBufferedReader(text4_cipher);
       String text5 = a.readUsingBufferedReader(text5_cipher);
       String text10 = a.readUsingBufferedReader(text10_cipher);
       String te = a.readUsingBufferedReader(text_cipher);
       text = text.replaceAll("ё", "е");
       text = text.replaceAll("Ё", "Е");
       text = text.replaceAll("[^а-яА-Я]", "");
       text = text.replaceAll("\\s{1,}", " ").trim();
       text = text.toLowerCase();
       Decryption DE = new Decryption(te);
       System.out.println("------------------------------------");
       System.out.println("             Задание 1");
       System.out.println("------------------------------------");
       /*String answer;
       //КЛЮЧ длинной 17
       Key key = new Key();
       Scanner in = new Scanner(System.in);
       answer = in.nextLine();
       System.out.println("OK, ключ - " + key.ChoosenKey(answer));
       Encrypt en = new Encrypt();
       WriteFile wr1 = new WriteFile(en.encrypt(textArray, alpha, answer), key.ChoosenKey(answer));
       Key key_3 = new Key();
       answer = in.nextLine();
       System.out.println("OK, ключ - " + key_3.ChoosenKey(answer));
       Encrypt en_3 = new Encrypt();
       WriteFile wr2 = new WriteFile(en_3.encrypt(textArray, alpha, answer), key_3.ChoosenKey(answer));
       Key key_4 = new Key();
       answer = in.nextLine();
       System.out.println("OK, ключ - " + key_4.ChoosenKey(answer));
       Encrypt en_4 = new Encrypt();
       WriteFile wr3 = new WriteFile(en_4.encrypt(textArray, alpha, answer), key_4.ChoosenKey(answer));
       Key key_5 = new Key();
       answer = in.nextLine();
       System.out.println("OK, ключ - " + key_5.ChoosenKey(answer));
       Encrypt en_5 = new Encrypt();
       WriteFile wr4 = new WriteFile(en_5.encrypt(textArray, alpha, answer), key_5.ChoosenKey(answer));
       Key key_6 = new Key();
       answer = in.nextLine();
       System.out.println("OK, ключ - " + key_6.ChoosenKey(answer));
       Encrypt en_6 = new Encrypt();
       WriteFile wr5 = new WriteFile(en_6.encrypt(textArray, alpha, answer), key_6.ChoosenKey(answer));*/

       System.out.println("------------------------------------");
       System.out.println("             Задание 2");
       System.out.println("------------------------------------");
       System.out.print("Индекс для для ВТ : ");
       Index inde = new Index(text);
       System.out.print("Индекс для длины 2: ");
       Index inde2 = new Index(text2);
       System.out.print("Индекс для длины 3 : ");
       Index inde3 = new Index(text3);
       System.out.print("Индекс для длины 4: ");
       Index inde4 = new Index(text4);
       System.out.print("Индекс для длины 5: ");
       Index inde5 = new Index(text5);
       System.out.print("Индекс для длины 10: ");
       Index inde10 = new Index(text10);
    }
}

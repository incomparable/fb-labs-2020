package com.company;

import static java.lang.String.valueOf;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class Decryption extends Index {
    static char[] alpha = new char []{'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'};
    public static double[] freq = new double[32];
    public static void blocks (String text) {
        char[] charText = text.toCharArray();
        String[] keyBlocks = new String[34];
        for (int j = 2; j <= 32; j++) {
            String block = "";
            for (int i = j-2; i < charText.length; i += j) {
                block += charText[i];
            }
            System.out.print(j + " ");
            Index decr = new Index(block);
            keyBlocks[j] = block;
        }
        char[] keyText = keyBlocks[17].toCharArray();
        for (int i = 0 ; i < 17 ; i++) {
            String AgainBlock = "";
            for (int j = i ; j < keyText.length; j= j + 16) {
                AgainBlock += keyText[j];
            }
        }

    }
    public static void mostFrequencyLetter(String text) {
        Map<Character, Integer> freq = new HashMap<>();
        for(char c : text.toCharArray()) {
            if(Character.isLetter(c)) {
                if(!freq.containsKey(c))
                    freq.put(c, 1);
                else
                    freq.put(c, freq.get(c) + 1);
            }
        }
        int maxValueInMap=(Collections.max(freq.values()));
        for (Map.Entry<Character, Integer> entry : freq.entrySet()) {
            if (entry.getValue() == maxValueInMap) {
                System.out.println("Наиболее часто встречающаяся буква: " + entry.getKey());
                break;
            }
        }
    }
    private static String decrypt(String encryptedMessage, String key) {
       char[] keyText = key.toCharArray();
       char[] encrypted = encryptedMessage.toCharArray();
       int decrypted;
       String decryptedMessage = "";
       for (int i = 0 ; i < encryptedMessage.length()-1; i++) {
           decrypted = ((encrypted[i] - keyText[i%17] + 32)%32);
           decryptedMessage += alpha[decrypted];
       }
       return decryptedMessage;
    }
    Decryption(String text) {
        blocks(text);
        String key = "войнамагаэндшпиль";
        System.out.println(decrypt(text, key));
    }

}
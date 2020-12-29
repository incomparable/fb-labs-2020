package com.company;

public class Encrypt {
   public static String encrypt(char text[], char alph[], String key) {
        int y;
        char[] keyArray = key.toCharArray();
        String enc = "";
        for (int i = 0 ; i < text.length-1; i++) {
            y = (text[i] + keyArray[i % (keyArray.length)])%32;
            enc += alph[y];
        }
        return enc;
    }
    Encrypt(){}
}

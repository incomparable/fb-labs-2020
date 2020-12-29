package com.company;

import java.io.*;

public class WriteFile {
    WriteFile(String text, String key)throws IOException{
        try (
                Writer writer = new BufferedWriter(new OutputStreamWriter(
                        new FileOutputStream("C:\\Users\\What Is Love\\Desktop\\Lab2_CRYPTO\\src\\com\\company\\" + "ключ_"+ key + ".txt"), "utf-8"))) {
            writer.write(text);
        }
    }
}

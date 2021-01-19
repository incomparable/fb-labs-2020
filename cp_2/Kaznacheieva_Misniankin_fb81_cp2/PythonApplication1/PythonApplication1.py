from collections import Counter
from itertools import cycle
import re
import math


key_1 = 'да'
key_2 = 'нет'
key_3 ='семь'
key_4 = 'кошка'
key_5 = 'декоммунизация'


alpha = [chr(i) for i in range(ord('а'),ord('я')+1)]


def encrypt(file,result_file, key):
    fin = open (file, "rt", encoding="utf-8")
    fout = open(result_file, "wt", encoding="utf-8")
    text = fin.read()
    #print(text)
    txt=''
    n=0
    for i in range(0, len(text)):
        if text[i] in alpha:
            txt=alpha[(alpha.index(text[i])+alpha.index(key[n%len(key)]))%32]
            n+=1
            #print(n)
            fout.write(txt)
            #print (txt)

  
def decrypt(file,result_file, key):
    fin = open (file, "rt", encoding="utf-8")
    fout = open(result_file, "wt", encoding="utf-8")
    text = fin.read()
    print(text)
    dtxt=''
    n=0
    for i in range(0, len(text)):
        if text[i] in alpha:
            dtxt=alpha[(alpha.index(text[i])-alpha.index(key[n%len(key)])+len(alpha))%32]
            n+=1
           # print(n)
            fout.write(dtxt)
            #print (dtxt)


def count_frequency(text):
    frequency = {}
    count = Counter(text)
    for i in count:
        frequency[i] = count[i]
    return frequency

def count_index(filename):
    f = open(filename)
    text = f.read()
    leng = len(text)
    if leng == 1:
        result = 1 / ((leng) * leng)
    else:
        result = 1 / ((leng - 1) * leng)

    freq = count_frequency(text)
    sum = 0
    for letter in freq:
        sum += freq[letter] * (freq[letter] - 1)
    c=result*sum
    print(c)
    return c

def divided(fulltext, n):
    return [fulltext[i:i + n] for i in range(0, len(fulltext), n)]


def find_key(filename):
    fin= open (filename, "rt", encoding="utf-8")
    fulltext = fin.read()
    for i in range(2, 30):
        parttext = divided(fulltext, i)
        temp = ""
        for n in parttext:
            temp = temp + n[0]
        sum_of_blocks = count_index(temp)
        print("i = ", i, "index = ", sum_of_blocks)

def most_freq_letter(frequency):
    max_val = max(frequency.values())

    return get_key(frequency, max_val)


def get_key(let, value):
    for k, v in let.items():
        if v == value:
            return k


def search_key(filename, len_of_key):
    fin = open (filename, "rt", encoding="utf-8")
    fout = open('results.txt', "wt", encoding="utf-8")
    text = fin.read()
    key_list = divided(text, len_of_key)
    russian_most_used = ('о','а','е','и','т','н','с','р', 'л')
    print (russian_most_used)
    for let in russian_most_used:
        res = ""
        for i in range(0, len_of_key):
           temp = ""
           for n in key_list:
                if len(n) > i:
                    temp = temp + n[i]
           ll = most_freq_letter(count_frequency(temp))
           key = (ord(ll) - ord(let)) % 32 + 1072
           res = res + chr(key)
           print("With ", let, "result is", res, '\n')
           fout.write(res)




#find_key('text.txt')
#search_key('text.txt', 15)
encrypt('justtext.txt', 'encryptedst.txt', key_5)
count_index('encryptedst.txt')
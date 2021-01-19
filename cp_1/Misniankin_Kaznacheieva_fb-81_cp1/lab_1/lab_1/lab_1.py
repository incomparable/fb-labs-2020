from collections import Counter
import re
import math
import codecs

alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ')

def ord(letter):
    if letter in alpha:
        #print(alpha.index(letter))
        return alpha.index(letter)
def chr(index):
    if index <= len(alpha):
        #print(alpha[index])
        return alpha[index]

def removesym(first): # удаление всех символов, кроме кириллицы и пробела
    alpha = ('А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
             'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з',
             'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
             'э', 'ю', 'я', ' ')
    fin = open(first, encoding="utf-8")
    fout = open('result.txt', "wt", encoding="utf-8")

    for bukva in fin.read():
        if bukva in alpha:
            fout.write(bukva)



def remove2spaces(filename):
    f = open(filename, 'r+', encoding="utf-8")
    text = ''.join([line.replace(u"  ", u" ") for line in f.readlines()])
    f.seek(0)
    f.write(text)
    f.close()


def remove1space(filename):
    f = open(filename, 'r+', encoding="utf-8")
    text = ''.join([line.replace(u" ", u"") for line in f.readlines()])
    f.seek(0)
    f.write(text)
    f.close()


def replace_e(filename):  # Замена ё на е
   f = open(filename, 'r+', encoding="utf-8")
   text = ''.join([line.replace(u"ё", u"е") for line in f.readlines()])
   f.seek(0)
   f.write(text)
   f.close()


def replace_b(filename):  # Замена ъ на ь
    f = open(filename, 'r+', encoding="utf-8")
    text = ''.join([line.replace(u"ъ", u"ь") for line in f.readlines()])
    f.seek(0)
    f.write(text)
    f.close()

def big_to_lower(filename): #,большие на маленькие
    f = open(filename, 'r+', encoding="utf-8")
    text = ''.join([line.lower() for line in f.readlines()])
    f.seek(0)
    f.write(text)
    f.close()   


def freq_count(filename):  # Частота букв в тексте
    alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ')
    let_count = 0
    fin = open(filename)
    for let in fin.read():
                let_count = let_count + 1 
    fin.close()
    temp_count = 0
    for c in alpha:
        fin = open(filename)
        with open(filename, 'r+',  encoding="utf-8", errors='ignore') as f:
            text = f.read()
            chast = text.count(c)*100*2/let_count
        print (c, chast, end='\n')



def bigram_counter(filename):  # Подсчет количества биграмм с пересечениями
    f = open(filename, 'r+',  encoding="utf-8")
    fout = open('file.csv', 'r+',  encoding="utf-8")
    text = f.read().replace('\n', '')
    k = len(text) - 1
    s = re.findall(r'(?=([а-я]{2}))', k)
    t = Counter(s)
    l = list()
    for bgr in s:
        t[bgr]+=1
    t.most_common()
    p = t.most_common()
    k = p.sort()
    print (k)
    l.extend(k)
    fout.write(l)


def bigram_counter_2(filename):  # биграммы без пересечений
    f = open(filename, 'r+',  encoding="utf-8")
    fout = open('file.csv', 'r+',  encoding="utf-8")
    text = f.read().replace('\n', '')
    k = round(len(text)/2)
    s = re.findall(r'(?=([а-я]{2}))', k)
    t = Counter(s)
    l = list()
    for bgr in s:
        t[bgr]+=1
    t.most_common()
    p = t.most_common()
    k = p.sort()
    print (k)
    l.extend(k)
    fout.write(l)



def H1(filename):  # H1
    alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
             'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я')
    let_count = 0
    fin = open(filename)
    for let in fin.read():
                let_count += 1 
    temp_count = 0
    H = 0
    fin.close()
    for c in alpha:
        with open(filename, 'r+',  encoding="utf-8", errors='ignore') as f:
            text = f.read()
            for let in text:
                if c == let:
                    temp_count += 1
            if temp_count != 0:
                chast = temp_count/let_count
                H -= chast * math.log2(chast)
    temp_count = 0

    print('H1=', H)
    f.close()

def H2_1(filename):  # H2 с пересечениями
    f = open(filename, 'r+',  encoding="utf-8")
    fout = open('file.csv', 'r+',  encoding="utf-8")
    text = f.read().replace('\n', '')
    k = round(len(text) / 2)
    s = re.findall(r'(?=([а-я]{2}))', k)
    t = Counter(s)
    l = list()
    for bgr in s:
        t[bgr]+=1
    t.most_common()
    p = t.most_common()
    k = p.sort()
    print (k)
    l.extend(k)

    H = 0

    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] != 0:
                H -= l[i][j] / k * math.log2(l[i][j] / k) / 2

    print("H2 c пересечениями =",H)


def H2_2(filename):  # H2 без пересечений

    f = open(filename, 'r+',  encoding="utf-8")
    fout = open('file.csv', 'r+',  encoding="utf-8")
    text = f.read().replace('\n', '')
    k = round(len(text) / 2)
    s = re.findall(r'(?=([а-я]{2}))', k)
    t = Counter(s)
    l = list()
    for bgr in s:
        t[bgr]+=1
    t.most_common()
    p = t.most_common()
    k = p.sort()
    print (k)
    l.extend(k)

    H = 0

    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] != 0:
                H -= l[i][j] / k * math.log2(l[i][j] / k) / 2
    print("H2 без пересечений =",H)






def R(S):
        R = 0
        R = 1 - (S/math.log2(32))
        print (R)


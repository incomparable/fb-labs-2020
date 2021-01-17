from collections import Counter
import re
import math
import codecs

alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ')

def ord(let):
    if let == 'а': return 0
    if let == 'б': return 1
    if let == 'в': return 2
    if let == 'г': return 3
    if let == 'д': return 4
    if let == 'е': return 5
    if let == 'ж': return 6
    if let == 'з': return 7
    if let == 'и': return 8
    if let == 'й': return 9
    if let == 'к': return 10
    if let == 'л': return 11
    if let == 'м': return 12
    if let == 'н': return 13
    if let == 'о': return 14
    if let == 'п': return 15
    if let == 'р': return 16
    if let == 'с': return 17
    if let == 'т': return 18
    if let == 'у': return 19
    if let == 'ф': return 20
    if let == 'х': return 21
    if let == 'ц': return 22
    if let == 'ч': return 23
    if let == 'ш': return 24
    if let == 'щ': return 25
    if let == 'ь': return 26
    if let == 'ы': return 27
    if let == 'э': return 28
    if let == 'ю': return 29
    if let == 'я': return 30

def chr (num):
    if num == 0: return 'а'
    if num == 1: return 'б' 
    if num == 2: return 'в'
    if num == 3: return 'г' 
    if num == 4: return 'д' 
    if num == 5: return 'е' 
    if num == 6: return 'ж' 
    if num == 7: return 'з' 
    if num == 8: return 'и'
    if num == 9: return 'й' 
    if num == 10: return 'к' 
    if num == 11: return 'л' 
    if num == 12: return 'м' 
    if num == 13: return 'н' 
    if num == 14: return 'о' 
    if num == 15: return 'п'
    if num == 16: return 'р'
    if num == 17: return 'с'
    if num == 18: return 'т'
    if num == 19: return 'у'
    if num == 20: return 'ф'
    if num == 21: return 'х'
    if num == 22: return 'ц'
    if num == 23: return 'ч'
    if num == 24: return 'ш'
    if num == 25: return 'щ'
    if num == 26: return 'ь'
    if num == 27: return 'ы'
    if num == 28: return 'э'
    if num == 29: return 'ю'
    if num == 30: return 'я'


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



def frequency(matrix, bigram_counter):
    alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ')
    for i in range(len(matrix)):
        print(alpha[i], end=' ')
        for j in range(len(matrix[i])):
            print("{:10f}".format(round(matrix[i][j] * 100 / bigram_counter, 6)), end="")
        print()


def bigram_counter(filename):  # Подсчет количества биграмм с пересечениями
    with open(filename, 'r+',  encoding="utf-8", errors='ignore') as f:
        text = f.read().replace('\n', '')

    matrx = [[0] * 33 for i in range(33)]

    bigram_counter = len(text) - 1

    for bukva in range(len(text) - 100):
        if text[bukva] != ' ' and text[bukva + 1] != ' ':
            matrx[ord(text[bukva])][ord(text[bukva + 1])] += 1
        if text[bukva] == ' ' and text[bukva + 1] != ' ':
            matrx[32][ord(text[bukva + 1])] += 1
        if text[bukva] != ' ' and text[bukva + 1] == ' ':
            matrx[ord(text[bukva])][32] += 1

    alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
             'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я')
    for bukva in alpha:
        print('       ', bukva, end=' ')
    print()
    frequency(matrx, bigram_counter)


def bigram_counter_2(filename):  # биграммы без пересечений
    with open(filename, 'r+',  encoding="utf-8", errors='ignore') as f:
        text = f.read()
    matrx = [[0] * 33 for i in range(33)]

    bigram_counter = round(len(text) / 2)

    for bukva in range(round((len(text) - 100) / 2)):
        if text[bukva * 2] != ' ' and text[bukva * 2 + 1] != ' ':
            matrx[ord(text[bukva * 2])][ord(text[bukva * 2 + 1])] += 1
        if text[bukva * 2] == ' ' and text[bukva * 2 + 1] != ' ':
            matrx[32][ord(text[bukva * 2 + 1])] += 1
        if text[bukva * 2] != ' ' and text[bukva * 2 + 1] == ' ':
            matrx[ord(text[bukva * 2])][32] += 1

    alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я')
    for bukva in alpha:
        print('       ', bukva, end=' ')
    print()
    frequency(matrx, bigram_counter)


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
    with open(filename, 'r+',  encoding="utf-8", errors='ignore') as f:
        text = f.read()
    matrx = [[0] * 33 for i in range(33)]

    bigramm_counter = len(text) - 1

    for bukva in range(len(text) - 2):
        if text[bukva] != ' ' and text[bukva + 1] != ' ':
            matrx[ord(text[bukva])][ord(text[bukva + 1])] += 1
        if text[bukva] == ' ' and text[bukva + 1] != ' ':
            matrx[32][ord(text[bukva + 1])] += 1
        if text[bukva] != ' ' and text[bukva + 1] == ' ':
            matrx[ord(text[bukva])][32] += 1

    H = 0

    for i in range(len(matrx)):
        for j in range(len(matrx[i])):
            if matrx[i][j] != 0:
                H -= matrx[i][j] / bigramm_counter * math.log2(matrx[i][j] / bigramm_counter) / 2

    print("H2 c пересечениями =",H)


def H2_2(filename):  # H2 без пересечений

    with open(filename, 'r+',  encoding="utf-8") as f:
        text = f.read()
    matrx = [[0] * 33 for i in range(33)]

    bigramm_counter = round(len(text) / 2)

    for bukva in range(round((len(text) - 100) / 2)):
        if text[bukva * 2] != ' ' and text[bukva * 2 + 1] != ' ':
            matrx[ord(text[bukva * 2])][ord(text[bukva * 2 + 1])] += 1
        if text[bukva * 2] == ' ' and text[bukva * 2 + 1] != ' ':
            matrx[32][ord(text[bukva * 2 + 1])] += 1
        if text[bukva * 2] != ' ' and text[bukva * 2 + 1] == ' ':
            matrx[ord(text[bukva * 2])][32] += 1

    H = 0

    for i in range(len(matrx)):
        for j in range(len(matrx[i])):
            if matrx[i][j] != 0:
                H -= matrx[i][j] / bigramm_counter * math.log2(matrx[i][j] / bigramm_counter) / 2

    print("H2 без пересечений =",H)






def R(S):
        R = 0
        R = 1 - (S/math.log2(32))
        print (R)


#removesym('text.txt')
#remove2spaces('result.txt')
#remove1space('textnospaces.txt')
#replace_e('textnospaces.txt')
#replace_b('textnospaces.txt')
#big_to_lower('textnospaces.txt')
#freq_count('result.txt')
#count_let('textnospaces.txt')
#bigram_counter('result.txt')
#bigram_counter_2('result.txt')
#H1('resultnospaces.txt')
#H2_1('resultnospaces.txt')
#H2_2('resultnospaces.txt'

#R(1.5953)
#R(2.3102) 

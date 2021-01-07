#!/usr/bin/env python3

from collections import Counter
import codecs
import operator
f1_f = open("clear.txt", encoding='utf-8', mode="r")
f1 = f1_f.read()
alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

keys = ["оп", "сбу", "сзру", "порох", "зелень", "радикал", "зрадники", "скотиняка", "дссззиусбу", "голосуйзапорошенка"]

def encrypt(text,key):
    changed = []
    index = 0
    for i in text:
        n = alph.find(i)
        n += alph.find(key[index])
        n = n%len(alph)
        changed.append(alph[n])
        index +=1
        if index == len(key):
            index = 0
    return ''.join(changed)


def decrypt(text,key):
    changed = []
    index = 0

    for i in text:
        n = alph.find(i)
        n -= alph.find(key[index])
        n = n%len(alph)
        changed.append(alph[n])
        index +=1
        if index == len(key):
            index = 0
    return ''.join(changed)


def one_letter_frequency(t):
    letter = [i for i in range(len(alph))]
    for i in t:
        letter[alph.find(i)] += 1
    return letter



def index(ctext,length):
    res = 0.0
    fin = 0.0
    l = one_letter_frequency(ctext)
    for i in l:
        res += i*(i-1)
    res *= 1.0/(float(length)*(float(length)-1))
    return res
print('[ * ] Open text indexes:',index(f1,len(f1)))
#encrypt
print('[ * ] Encrypted text index:')
for key1 in keys:
    f2_s = encrypt(f1, key1)
    with open("enc_" + str(len(key1)) + ".txt", encoding='utf-8', mode="w") as f2_f:
        print(len(key1),index(encrypt(f2_s, key1),len(f2_s)))
        f2_f.write(f2_s)

cptext = open('shifr_text_var17.txt','r').read()

cptext = cptext.replace('\n','')

maintable = dict()

print('[ * ] Blocks index:')
def create_block_ic(t,n):
    l = []
    if len(t)%n != 0:
        t = t[:-(len(t)%n)]
    for i in range(n):
        r = ''
        for j in range(i,len(t),n):
            r+=t[j]
        l.append(r)
    return l

for i in range(2,31):
    p = 0.0
    for j in create_block_ic(cptext,i):
        p += index(j,len(j))
    maintable[i] = p/i
for key,value in maintable.items():
    print(key, value)
keylength = max(maintable.items(), key=operator.itemgetter(1))[0]

keylength =int(keylength/2)
print("[ * ] Key length -- ", keylength)

key = []

for i in create_block_ic(cptext,keylength):
    index, value = max(enumerate(one_letter_frequency(i)), key=operator.itemgetter(1))
    keyitem = index - alph.find('о')
    key.append(alph[keyitem])

print( '[ i ] Key: ',''.join(key))

cl_text = decrypt(cptext,'абсолютныйигрок')
with open("dec.txt", encoding='utf-8', mode="w") as f4_decr:     f4_decr.write(cl_text)
k = 0
d1 = {}
d2 = {}

for i in one_letter_frequency(cl_text[1::14]):
    d1[alph[k]] = i
    k+=1

print('[ i ] Decrypted text: ',cl_text)

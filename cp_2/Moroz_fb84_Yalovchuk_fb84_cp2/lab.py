#!/usr/bin/env python3
import random
import numpy as np


f_txt=open( "text.tttxttt", 'r')
txt=f_txt.read().replace('\n','')

keys = ["ак", "йцу", "фыва", "понни", "ячсмитьбюлорйцу"]
alph="абвгдежзийклмнопрстуфхцчшщъыьэюя"

alph_len=ord("я")-ord("а")

def lett_freq(text):
    frq=[]
    for i in alph:
         frq.append( (i, text.count(i)))
    return frq

def decrypt(text, key):
    s=""
    for i in range(len(text)):
        s+=alph[( ord(text[i]) -2*1072 - ord(key[i%len(key)]) ) % (alph_len+1)]
    return s


def encode(phrase, key):
    s=""
    period=len(key)
    print( '---------------')
    print("key:\t\t{}\nperiod:\t\t{}".format(key, period))
    for i in range(len(phrase)):
        s+=alph[( ord(phrase[i]) -2*1072 + ord(key[i%period]) ) % (alph_len+1)]
    print("\nencrypted:\t", s)
    return s

def i_vidp(text):
    l_fr = lett_freq( text)
    #print(l_fr)
    index=0
    for i in range(len( l_fr)):
        index+=l_fr[i][1]*(l_fr[i][1]-1)
    index /= len(text)*(len(text)-1)
    return index

def chop(text, i_r):
    if len(text)%i_r != 0:
        text = text[:-(len(text)%i_r)]
    c=[]
    for i in range(i_r):
        y_i=''
        for i2 in range(i,len(text),i_r):
            y_i+=text[i2]
        c.append(y_i)
    return c

print("open:\t\t", txt)

print( i_vidp(txt) )

for i in keys:
    indx = i_vidp( encode( txt, i))
    print( indx ,"\n")

print( "0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0")
f_txt=open( "shifr_text_var17.txt", 'r')
c_txt=f_txt.read().replace('\n','')
indexes={}

#for i in range(2,31):
#    indexes[i]= i_vidp( encode( txt, ''.join(random.choice(alph) for x in range(i)) ))

#print( indexes)
#print( i_vidp(c_txt) )

max_ind={"value":0, "index":0}
for i_0 in range(2,33):
    sum_indexes=0
    for i in chop(c_txt, i_0):
        sum_indexes+=i_vidp(i)

    print("i: {}\tindex: {}".format(i_0, sum_indexes/i_0))
    if sum_indexes>max_ind["value"]:
        max_ind["index"]=i_0
        max_ind["value"]=sum_indexes


#print( max_ind)
key_l=int(max_ind[ "index"]/2)

print("key length: {}".format(key_l))

#for i in chop(txt, key_l):
#        frq=lett_freq(i)
#        max_frq_o={"value":0, "index":0}
#        for i_fr in alph:
#            if i.count(i_fr)>max_frq_o["value"]:
#                    max_frq_o["index"]=i_fr
#                    max_frq_o["value"]=i.count(i_fr)
#        print(max_frq_o)



key=''

for i in chop(c_txt, key_l):
        frq=lett_freq(i)
        max_frq={"letter":0, "value":0}
        for i_fr in alph:
            if i.count(i_fr)>max_frq["value"]:
                    max_frq["letter"]=i_fr
                    max_frq["value"]=i.count(i_fr)
        key+=(alph[alph.find(max_frq["letter"])-alph.find('о')])   

#print(decrypt( c_txt, key))
print("(not) key: {}".format(key))
print("real key: абсолютныйигрок")
print(decrypt( c_txt, "абсолютныйигрок"))



#print( chop("фывапр",4))

















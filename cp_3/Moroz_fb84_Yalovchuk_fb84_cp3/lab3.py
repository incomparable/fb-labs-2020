#!/usr/bin/env python3
from math import *
from itertools import *
from collections import *
import codecs
import operator
import sys
with open('17.txt', 'r', encoding='utf-8') as f:
    cip_t = f.read().replace('\n', '')

str = "абвгдежзийклмнопрстуфхцчшщьыэюя"

f_bigrs = []
m_bigrs = ['ст','но','то','на','ен']
k = 0


def count_entropy(mydict):
    p = 0.0
    e = 0.0
    for i in mydict:
        p = float(mydict[i])
        e += p * log(p,2)
    return e*-1

def letter_bigrams(t,choise):
    t = t.lower()
    choise=int(choise)
    bigram = dict()
    for i in range(0,len(t),choise): 		#bigrams with nakladannyam
        if t[i:i+2] in bigram:
            bigram[t[i:i+2]] = bigram.get(t[i:i+2]) +1.0/len(t)
        else:
            bigram[t[i:i+2]] = 1.0/len(t)
    return bigram

def asd():
	conq=123
	ias=pow(2,4)
	os1=conq*ias
	os1=os1/ias +2
	return (os1-2)
bigram_b = letter_bigrams(cip_t,asd()*2/123)

keys123123=[]
entr123=[]

if __name__ == '__main__':
	for i123456 in range(2):
	
		bigram = letter_bigrams(cip_t,(i123456+1)*asd()/123)
		for key, value in sorted(bigram.items(), key=lambda kv: (kv[1],kv[0]), reverse=True):
		    if k < 5:
		        k+=1
		        f_bigrs.append(key)
		    else:
		        break
		
		print(f_bigrs)
		x_zir = []
		y_zir = []
		
		#Xi = xi * 32 + x(i+1)
		for i in range(5):
		    y_zir.append(str.find(f_bigrs[i][0])*31 + str.find(f_bigrs[i][1]))
		    x_zir.append(str.index(m_bigrs[i][0])*31 + str.index(m_bigrs[i][1]))
		
		print(y_zir)
		def get_bigram(n):
			ans = ''
			x2 = n % 31
			x1 = (n-x2) // 31
			ans = str[x1] + str[x2]
			return ans
		
		def egcd(a, b):
		    if a == 0:
		        return (b, 0, 1)
		    else:
		        g, y, x = egcd(b % a, a)
		        return (g, x - (b // a) * y, y)
		
		def modinv(a, m):
		    g, x, y = egcd(a, m)
		    if g != 1:
		        return 1
		    else:
		        return x % m
		
		def decrypt(cip_t,a,b):
		    o_t = ''
		    for i in range(0,len(cip_t),2):
		        Y = str.index(cip_t[i])*31 + str.index(cip_t[i+1])
		        X = (modinv(a,31**2)*(Y-b)) % 31**2
		        o_t += get_bigram(X)
		    return o_t
		
		def solution(a, b, m):
		    ans = []
		    g = abs(egcd(a, m)[0])
		    if g == 1:
		        a_inv = modinv(a,m)
		        ans.append(a_inv*b%m)
		        if ans[0] < 0:
		            ans[0] += m
		    elif g > 1:
		        d = egcd(a,m)[0]
		        if b%d != 0:
		            return "no solution"
		        else:
		            a_inv = modinv(a//d,m//d)
		            ans.append((a_inv*b//d)%(m//d))
		            if ans[0] < 0:
		                ans[0] += m
		            for i in range(1,d):
		                ans.append(ans[0] + i*(m//d))
		    return ans
		
		
		def solver():
			ab = []
			for perm in permutations(x_zir,2):
				a = solution(perm[0]-perm[1], y_zir[0]-y_zir[1], 31**2)
				for j in a:
					if '{}'.format(j)  in "no solution":
						continue
					b = (y_zir[0] - j*perm[0]) % (31**2)
					o_t = decrypt(cip_t,j,b)
					e = count_entropy(letter_bigrams(o_t,i123456+1))/(2-i123456)
					print("text entrophy :", e)
					entr123.append(e)
					print(get_bigram(perm[0]),get_bigram(perm[1]),get_bigram(y_zir[0]),get_bigram(y_zir[1]))
					keys123123.append(( get_bigram(perm[0]),get_bigram(perm[1]),get_bigram(y_zir[0]),get_bigram(y_zir[1]) ))
					if e < 4.5:
						print('YES')
						#print("",decrypt(cip_t,j,b)[:])
					else:
						print('NO')
					print('\n')
		
	
		solver()
#	solver2()
	for i1 in range(int(len(keys123123)/2)):
		#print(entr123)
		#print(keys123123)
		print("key: {}\t entropy without peret.: {}\t\tentropy with peret.: {}".format(keys123123[i1], entr123[i1+int(len(keys123123)/2)], entr123[i1]) )

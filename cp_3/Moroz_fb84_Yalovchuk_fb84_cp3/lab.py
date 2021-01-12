#!/usr/bin/env python3

import math
from itertools import combinations
from itertools import permutations
from collections import Counter

with open("./17.txt",'r') as f: f_s=f.read().replace('\n','')

alph="абвгдежзийклмнопрстуфхцчшщьыэюя"
m=31
most_fr_b_lang = ["ст", "но", "по", "то", "на" ]
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)

def obern(a, n):
    try:
        g, x, _ = egcd(a[0], n)
    except:
        g, x, _ = egcd(a, n)
    if g != 1:
        return "-"
    return x % n

def solve(a,b,n):

    #a*x=b%n
    x=[]
    if egcd(a,n)[0]==1:
        x.append((obern(a,n)*b)%n)
    else:
        d, _, _ = egcd(a,n)
        a1=a/d
        n1=n/d
        x=[]
        if b%d == 0:
            b1=b/d
            x.append(( obern(a1, n) * b1) % n1)
            for i in range(d):
                x.append(x[0]+i*n1)
        else:
            return "-"
    return x

def split_bigrs_wo_cross(str2):
    res = Counter(str2[idx: idx + 2] for idx in range(len(str2) - 1))
    return res
    


def most_fr_b_ct(str2):
    res = Counter(str2[idx: idx + 2] for idx in range(0,len(str2) - 1,2)) 
    most_fr = []
    for k in sorted(res, key=res.get, reverse=True)[:5]:
        most_fr.append(k)
    return res, most_fr

def count_entr( dec):
    res = split_bigrs_wo_cross(dec)
    sum2 = 0
    sum1 = sum(res.values())
    for i in list(res.keys()):
        sum2 = sum2 + (res[i]/sum1)*math.log2(res[i]/sum1)
    return -sum2/2

def solve_sys(xz, xzz, yz, yzz):
    xz  = (alph.find(xz[0])*m  + alph.find(xz[1]))%(m*m)
    xzz = (alph.find(xzz[0])*m + alph.find(xzz[1]))%(m*m)
    yz  = (alph.find(yz[0])*m  + alph.find(yz[1]))%(m*m)
    yzz = (alph.find(yzz[0])*m + alph.find(yzz[1]))%(m*m)
    a = solve((xz-xzz)%(m*m), (yz-yzz)%(m*m),m*m)
    b=[]
    sol=[]
    if a[0]=='-':
        return "-",'-'
    else:
        for i in a:
            b= (yz-i*xz)%(m*m)
            sol.append((i,b))
        return sol

def decrypt(cip_t, a, b):
    decr=""
    for i in range(0,len(cip_t)-1,2):
        yi= alph.index(cip_t[i])*m+alph.index(cip_t[i+1])
        if obern(a, m* m) != '-':
            try:
                xi = ( obern(a, m*m )*(yi-b )) % (m* m )
            except:
                xi = ( obern(a[0], m*m)*(yi-b )) % (m* m )
        else:
            return "sorry"
        xi=int(xi)
        decr+=alph[xi//31]+alph[xi%31]
    return decr

print(count_entr(f_s))
def main_pr():
    res, mst_fr = most_fr_b_ct( f_s)
    print(mst_fr)
    perm_y = permutations(mst_fr, 2) 
    perm_x = permutations(most_fr_b_lang, 2)
    perm_x = list(perm_x)
    perm_y = list(perm_y)
    
    for i1 in perm_x[0:]:
        for i2 in perm_y[0:]:
            #comb = combinations([i1[0], i1[1], i2[0], i2[1]], 4)
            #for j123 in (list(comb)):
            sol = solve_sys(i1[0], i1[1], i2[0], i2[1])
            try:
                for a,b in sol:
                    if a=='-':
                        continue
                    dec=decrypt(f_s, a, b)
                    if dec=='sorry':
                        continue
                    if(count_entr( dec) >4.3):
                        continue
                    else:
                        #pass
                        #print("yes")
                        print(i1,i2)
                        print(a,b)
                        #print('entropy: ',count_entr(dec))
                        print(dec[:500])
                        return dec
                        break
                    #print(j123)
            except:
                continue


decrypted_text = main_pr()

with open("./17_dec.txt",'w') as f2: f2.write(decrypted_text)


#!/usr/bin/env python3

from random import randrange, randint
from math import log
from pwn import *
import requests


def gcd(a,b):
    if a%b==0:
        return b
    return gcd(b,a%b)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)
def Mil_Rabin( p):
   #p-1=d*2^s
    d=p-1
    s=0
    if p % 2 == 0:
        return 0
    while d%2 == 0:
        d//=2
        s+=1
    
    d=int(d)
    k=5
    a1=0
    for _ in range(k):
        x=randint(2,p-2)
        x=pow(x, d,p)
        #x = random.randrange(2, p - 1)
        if( gcd(x,p) > 1):
            return 0
        if x == 1 or x == p - 1:
            continue 
        for _ in range(s - 1): 
            x = pow(x, 2, p) 
    
            if x == p - 1: 
                break 
        else: 
                return 0
    return 1

    # while a1<k:   
    #        a1+=1
    #        x=randint(2,p-2)
    #
    #        if( gcd(x,p) > 1):
    #            return 0
    #        x = power(x, d, p); 
    ##        x = (x**(d))%p 
    #        if x == 1 or x==-1%p:
    #            continue
    #
    #        is_get_answ=0
    #        while(d!=p-1):
    #            d*=2
    #            xi = (x**2)%p
    #            if(xi==1):
    #                return 0
    #            if(xi==p-1):
    #                continue
    #
    #        return 0
    #    return 0
    #

def gen_pr(mIn, mAx):
    p,q,p1,q1=4,4,4,4
    while(Mil_Rabin(p) ==0):
        p=randint(mIn, mAx)
    while(Mil_Rabin(q) ==0):
        q=randint(mIn, mAx)
    while(Mil_Rabin(p1) ==0):
        p1=randint(mIn, mAx)
    while(Mil_Rabin(q1) ==0):
        q1=randint(mIn, mAx)
    return [(p,q),(p1,q1)]


def find_d(e, fi):
    g, x, _ = egcd(e, fi)
    if g != 1:
        raise Exception('gcd(a, b) != 1')
    return x % fi

def GenerateKeyPair():
    pairs =  gen_pr(2**256,2**257)
    p=min(pairs[0])
    q=min(pairs[1])
    p1=max(pairs[0])
    q1=max(pairs[1])
    n=p*q
    n1=p1*q1
    fi_n = (p-1)*(q-1)

    #print("fi_n:\t0x%x\n"%fi_n)

    fi_n1 = (p1-1)*(q1-1)
    e=randint(2,n-2)
    e1=randint(2,n-2)
    while(egcd(e,fi_n)[0]>1 ):
        e=randint(2,n-2)
    while(gcd(e1,fi_n1)>1 ):
        e1=randint(2,n-2)
    d = find_d(e,fi_n)
    d1 = find_d(e1,fi_n1)
    return p, q, p1, q1, n, n1, e, e1, d, d1

def Encrypt(m, e, n):
    return pow(m, e, n)
    
def Decrypt(c, d, n):
    return pow(c, d, n)

def Sign(m, d, n):
    return pow(m, d, n)

def Verify(m,s,e,n):
    if pow(s,e,n) == m:
        return True
    else:
        return False

def SendKey(m, priv_key_a, o_keys_b):
    enc_msg= Encrypt(m, o_keys_b[0], o_keys_b[1])
    sign_a = Sign(m, priv_key_a[0], priv_key_a[1])
    encrypted_sign_a = Encrypt(sign_a, o_keys_b[0], o_keys_b[1])
    return enc_msg, sign_a, encrypted_sign_a
    
def RecievKey(enc_msg, sign_a, encrepted_sign_a, priv_keys_b, o_keys_a):
    dec_msg= Decrypt(enc_msg, priv_keys_b[0], priv_keys_b[1])
    Dec_b = Decrypt( encrepted_sign_a, priv_keys_b[0], priv_keys_b[1])
    verify_a = Verify(dec_msg, Dec_b, o_keys_a[0], o_keys_a[1])
    return (dec_msg, verify_a)



p, q, p1, q1, n, n1, e, e1, d, d1 = GenerateKeyPair()


print("q*p:\t0x%x* 0x%x"%(q,p))
print("q1*p1*:\t0x%x* 0x%x"%(q1,p1))
print("n*n1:\t0x%x* 0x%x"%(n,n1))
print("e*d:\t0x%x* 0x%x"%(e,d))
print("d1*e1:\t0x%x* 0x%x"%(d1,e1))

message = randint(2**10, 2**20)
print(message)
enc = Encrypt( message, e, n)
print("Encrypted with A open key by B:", enc)
dec = Decrypt( enc, d, n)
print("Decrypted with A secret key by A:", dec)
sign = Sign(message, d, n)
print("Signature: 0x%x"%sign)
print("Is verified: ", Verify(message, sign, e, n))

enc1 = Encrypt( message, e1, n1)
print("Encrypted with B open key by A:", enc1)
dec1 = Decrypt( enc1, d1, n1)
print("Decrypted with B secret key by B:", dec1)
sign1 = Sign(message, d1, n1)
print("Is verified: ", Verify(message, sign1, e1, n1))
print("Signature: 0x%x"%sign1)

print("Sending message 0x%x and verifying it"%message)
enc_msg, sign_a, encrepted_sign_a = SendKey(message, [d, p*q], [e1, n1])
resp = RecievKey(enc_msg, sign_a, encrepted_sign_a, [d1,p1*q1], [e,n])
print("Message: 0x%x\nVerify is %s"%(resp))


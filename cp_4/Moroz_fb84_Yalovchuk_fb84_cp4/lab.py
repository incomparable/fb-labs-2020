#!/usr/bin/env python3

from random import randrange, randint
from math import log

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

def MillerRabin(p):
    if p % 2 == 0:
        return False 
    k = 5
    d = p-1
    while d % 2 == 0:
        d = d // 2
    s = int(log((p-1)/d)/log(2))
    for counter in range(k):
        x = randrange(2, p-1)
        if egcd(x, p)[0] > 1:
            return False
        xr = pow(x,d,p)
        if xr == 1 or xr == -1:
            return True
        r = 0
        while xr != p-1:
            xr = pow(xr,2,p)
            if r == s-1:
            	return False
            else:
            	r+=1
    return True

def get_random_primes(range_min, range_max):
    pairs = []
    while len(pairs) != 4:
        rand_number = randrange(range_min, range_max)
        if MillerRabin(rand_number):
            pairs.append(rand_number)
    return pairs


def Encrypt(m,e,n):
    return pow(m,e,n)


def Sign(m,d,n):
    return Encrypt(m,d,n)


def Decrypt(c,d,n):
    return pow(c,d,n)

def SendKey(k,na,d,eb,nb):
    s = Sign(k,d,na)
    s1 = Encrypt(s,eb,nb)
    k1 = Encrypt(k,eb,nb)
    return s,s1,k1

def Verify(m,s,e,n):
    m1 = Decrypt(s,e,n)
    if m1 == m:
        return True
    else:
        return False


def RecieveKey(k1,s1,nb,db,ea,na):
    k = Decrypt(k1,db,nb)
    s = Encrypt(s1,db,nb)
    return Verify(k,s,ea,na)

def fnd_e(on):
	while True:
		e = randrange(2,on)
		if egcd(e,on)[0] == 1:
			return e


def GetKeyPairs():
    pairs = get_random_primes(2**255, 2**256)
    pairs.sort(key = int)
    p = pairs[0]
    p1 = pairs[1]
    q = pairs[2]
    q1 = pairs[3]
    n = p*q
    on = (p-1)*(q-1)
    n1 = p1*q1
    on1 = (p1-1)*(q1-1)
    e=fnd_e(on)
    d = modinv(e, on)
    e1=fnd_e(on1)
    d1 = modinv(e1, on1)
    return (q,q1,p,p1,e,d,n,e1,d1,n1)

if __name__ == '__main__':
	q,q1,p,p1,e,d,n,e1,d1,n1 = GetKeyPairs()
	print( "q:", hex(q))
	print( "q1:", hex(q1))
	print( "p:", hex(p))
	print( "p1:", hex(p1))

	print( "e:", hex(e))
	print( "d:", hex(d))
	print( "n:", hex(n))
	print( "e1:", hex(e1))
	print( "d1:", hex(d1))
	print( "n1:", hex(n1))
	print( "Encrypting msg...")
	c = Encrypt(0xdeadbeef,e,n)
	print(hex(c))
	print("Decrypting msg...")
	m = Decrypt(c,d,n)
	print(hex(m))
	
	openm = 0xbeef
	sign = Sign(openm,d,n)
	print('verifing')
	print('Dig_sig:{}\nOpen msg:{}'.format(hex(sign),hex(openm)))
	ver = Verify(openm, sign,e,n)
	print(ver)
	print( 'Sending Key...')
	
	s,s1,k1 = SendKey(0xbeeeebbeeb,n,d,e1,n1)
	print( 'Recieving Key...' )
	
	print( "k1: ", hex(k1))
	print( "s1: ", hex(s1))
	print( "nb: ", hex(n1))
	print( "db: ", hex(d))
	print( "ea: ", hex(e))
	print( "na: ", hex(n))
	print( RecieveKey(k1,s1,n1,d1,e,n))
	print( "data for server")
	sn = 4747007696146299372418065200622389997152509910270942925234844218626352657290661178527906664276605898089262050324628782780773046903698613918984576163809803
	se = 65537
	while sn < n:
		q,q1,p,p1,e,d,n,e1,d1,n1 = GetKeyPairs()
		print(n)
	ss,ss1,sk1 = SendKey(2695546391815984120850,n,d,se,sn)
	print( "e:", hex(e))
	print( "n:", hex(n))
	print( 'ss1: ', hex(ss1))
	print( 'sk1: ', hex(sk1))

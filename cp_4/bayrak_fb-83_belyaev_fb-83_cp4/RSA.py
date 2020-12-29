from random import *
from math import gcd
channel = None
def antielem(a, m, qn=[]):
    if gcd(a, m)!= 1:
        return None
    q = int((m - m%a)//a)
    m=m%a
    
    qn.append(q)
    if m==0:
        v = [0, 1]
        for i in range (0, len(qn)-1):
            v.append(v[i]-(qn[i]*v[i+1]))
        qn.clear()
        return v[len(v)-1]
        
    else:
        return antielem(m, a, qn)
    
    



    
def isHardPrime(p, x, s, d):
    if pow(x, d, p)==1 or pow(x, d, p)==-1+p or pow(x, d, p)==-1:
        return True
    else:
        for r in range(1, s):
            xr=pow(x,d*pow(2, r) , p)
            if xr==-1+p or xr==-1:
                return True
            if xr == 1:
                return False
        return False
def isPrime(p):
    for i in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 21, 37}:
        if p%i==0:
            return False

    n=p-1
    s=1
    while n%pow(2, s+1)==0:
        s+=1
    d=n//pow(2, s)
    for k in range(0,100):
        x = randrange(1, n, 1)
        if gcd(p, x)>1:
            return False

        if isHardPrime(p, x, s, d)==False:
            return False
    return True
        

    
        
    
    
def GeneratePrimeNumber(min, max):
    num = 6
    while isPrime(num)==False:
        num = randrange(min, max, 1)
        print(num)
    
    return num

def Encrypt(message, public_key):
        c = pow(message, public_key[1], public_key[0])
        return c
def Verify(message, public_key):
    if message[0] == pow(message[1], public_key[1], public_key[0]):
        return True
    else:
        return False
    
class Abonent:

    def __init__(self, klen):
        print("p")
        self.p = GeneratePrimeNumber(pow(2, klen), pow(2, klen+1))
        print("q")
        self.q = GeneratePrimeNumber(pow(2, klen), pow(2, klen+1))
        self.public_key = 0
        self.private_key = 0


    def GenerateKeyPair(self):
        n=self.p*self.q
        fn=(self.p-1)*(self.q-1)
        e=pow(2, 16)+1
        d = antielem(e, fn)
        d=d%fn
        self.public_key = [n, e]
        self.private_key = d
    def Decrypt(self, c):
        message = pow(c, self.private_key, self.public_key[0])
        return message
    def Sign(self, message):
        s = pow(message, self.private_key, self.public_key[0])
        return [message, s]
    def SendKey(self, aim):
        m = randrange(1, pow(2, 32), 1)
        key = aim.public_key
        m1=Encrypt(m, key)
        s=self.Sign(m)
        s=s[1]
        s1=Encrypt(s, key)
        message=[m1, s1]
        print("Sender")
        print("aim public key = ", key)
        print("m = ", m)
        print("m1 = ", m1)
        print("s = ", s)
        print("s1 = ", s1)
        print("message = ", message)
        global channel
        channel = message
    def RecieveKey(self, autor):
        global channel
        message = channel
        key = autor.public_key
        m = self.Decrypt(message[0])
        s = self.Decrypt(message[1])
        print("Reciever")
        print("m = ", m)
        print("s = ", s)
        print("Verified?: ", Verify([m, s], key))
print('Enter lenght of key')
klen = int(input())
a = Abonent(klen)
b = Abonent(klen)
if a.p*a.q<b.p*b.q:
    c=a
    a=b
    b=c
a.GenerateKeyPair()
b.GenerateKeyPair()



message = randrange(1, pow(2, 32), 1)
print("message : ", message)
key = a.public_key
c = Encrypt(message, key)
print("B send a message: ", c)
m = a.Decrypt(c)
print("A got a message: ", m)

signed = a.Sign(message)
print("B got a signed message: ", signed)
print("Is this message from A?: ", Verify(signed, key))
print("p = ", a.p)
print("q = ", a.q)
print("p1 = ", b.p)
print("q1 = ", b.q)
a.SendKey(b)
b.RecieveKey(a)
##Protocol(a, b)
##print("done")


import random

def gen_random(a,b):
    return random.randint(a,b)

def euclid_NSD(a,b):
    if a == 0:
        x, y = (0, 1)
        return b, x, y
    d, x1, y1 = euclid_NSD(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def NSD(a,b):
    r = euclid_NSD(a,b)
    return r[0]

def obernenyu(x,m):
    nsd = euclid_NSD(x,m)
    if nsd[0]==1:
      if x<=m: return nsd[1]
      if x>m: return nsd[2]
    else: return None



def Miller_Iter(d,p):
    a = 2 + gen_random(1,p-4);
    x = pow(a,d,p);
    if (x==1 or x==p-1):
        return True;
        
    while (d!=p-1):
        x=(x*x)%p;
        if (x==1):
            return False;
        if (x==p-1):
            return True ;   
        d *=2;

    return False;


def Miller_test(p):
    k = 40
    prosti = [2, 3, 5, 7, 11, 13, 17, 19]
    for i in prosti:
        if p%i == 0:
            return False;

    d = p-1;
    while (d%2 == 0):
        d //= 2;

    for i in range(k):
        if (Miller_Iter(d,p)==False):
            return False;

    return True;


def gen_prime(l): #>256
    a = 2**(l-1)+1
    b = 2**l-1
    i = 0
    while i==0:
        x = gen_random(a,b)
        if Miller_test(x):
            i = 1
    return x


def Gen_Pair_of_Keys(l):
    p = gen_prime(l);
    q = gen_prime(l);
    while p == q:
        q = gen_prime(l);
    n = p*q
    fi = (p-1)*(q-1)

    e = 2 + gen_random(1,fi-3);
    nsd = euclid_NSD(e,fi);
    while nsd[0]!=1:
        e = 2 + gen_random(1,fi-3);
        nsd = euclid_NSD(e,fi);

    d = obernenyu(e,fi)

    return [n,e,d]


def Encrypt(M,e,n):
    return pow(M,e,n);


def Decrypt(C,d,n):
    return pow(C,d,n);


def Sign(M,d,n):
    signature = pow(M,d,n);
    return [M,signature];



def Verify(M,signature,e,n):
    if (M==pow(signature,e,n)):
        return True;
    else:
        return False;
    

def SendKey(k,Ad,An,Be,Bn):
    s = pow(k,Ad,An);
    s1 = pow(s,Be,Bn);
    k1 = pow(k,Be,Bn);
    return [k1,s1]


def ReceiveKey(k1,s1,Bd,Bn,Ae,An):
    k = pow(k1,Bd,Bn);
    s = pow(s1,Bd,Bn);
    if Verify(k,s,Ae,An):
        return k
    else:
        return None



M = gen_prime(256)
print("M = "+str(M)+"\n")


A = Gen_Pair_of_Keys(256)
B = Gen_Pair_of_Keys(256)
while B[0]<A[0]:
    B = Gen_Pair_of_Keys(256)

print(A)
print(B)


server_n = int("0xC8C66D5F3124CFF18A6D710BA138AB8E8FB29A500368456D3759993F27366803",16)
server_e = int("0x10001",16)
print("server_e = "+str(server_e))
print("server_n = "+str(server_n)+"\n")


print(Encrypt(M,server_e,server_n))


print(Verify(int("75BCD15",16),int("75BE7D13A4011F9C34AABECE886256D5191B39976C310E6F49EF2A3168692924",16),server_e,server_n))

Sk = SendKey(123,A[2],A[0],B[1],B[0]);
print(ReceiveKey(Sk[0],Sk[1],B[2],B[0],A[1],A[0]))


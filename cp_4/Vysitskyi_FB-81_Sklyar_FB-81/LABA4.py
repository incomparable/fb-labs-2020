import math, sys, random, requests

def miller(k):
    r=150;
    p=0;
    t=k-1;
    if k == 2 :
        return(True)
    if k == 3 :
        return(True)
    elif k % 2 == 0:
        return(False)
    else:
        while t % 2 == 0:
            t = t // 2
            p += 1
        for n in range(r):
            a = random.randint (2, k-1)
            x = pow (a, t, k)
            i = 0
            if x == 1: continue
            elif x == k-1 : continue  # -1modk 
            while i < p - 1:
                x = pow (x, 2, k)
                if x == k - 1: break
                i = i + 1
            else: return(False)
        return(True)

def prime_test(rand):
    if rand%2 == 0:
        return False
    elif rand%3 == 0:
        return False
    elif rand%5 == 0:
        return False
    elif rand%7 == 0:
        return False
    elif rand%11 == 0:
        return False
    if miller(rand) == False:
        print('%s is not a prime number, will find more.'% hex(rand))
        return False
    return rand 

def r_number(s):
    number = 2**(s-1)
    for k in range(1,s-1,1):
        b=random.randint(0,1)
        number += ((2**k)*b)
    number = number + 1
    return number

def mass_gen(s):
    rand_mass = []
    for k in range (0,2,1):
        rand=r_number(s)
        while prime_test(rand) == False:
            rand = r_number(s)
        rand_mass.append(rand)
    return rand_mass

def EulerFunc(n):
    f = n;
    if n%2 == 0:
        while n%2 == 0:
            n = n // 2;
        f = f // 2;
    i = 3
    while i*i <= n:
        if n%i == 0:
            while n%i == 0:
                n = n // i;
            f = f // i;
            f = f * (i-1);
        i = i + 2;
    if n > 1:
        f = f // n;
        f = f * (n-1);
    return f;

def gcd (k,n):
    if n == 0:
        return k
    else:
        return gcd(n, k%n)
    
def ev_alg(k,n):
    if k == 0: return (n,0,1)
    else: d,x,y = ev_alg(n%k, k)
    return (d,y-(n//k)*x,x)
    
def inverse(k,n):
    d,x,y = ev_alg(k,n)
    if d == 1:
        return x%n
    
def keygen(pq):
    n=int(pq[0])*int(pq[1])
    e=0
    Euler=(pq[0]-1)*(pq[1]-1)
    while gcd(e,Euler)!=1:
        e=random.randint(2,Euler-1) 
    d=inverse(e,Euler)
    o_k=[n,e]
    s_k=[d,pq,n]
    return(o_k,s_k)

def enc(msg, o_k):
    EN = pow(msg,o_k[1],o_k[0])
    return EN

def dec(EN, s_k):
    DM = pow(EN, s_k[0], s_k[2])
    return DM

def dig_s(MS, k, n):
    DS = pow(MS, k, n)
    return DS

def verify (DS, DM, o_k):
    print(o_k)
    if DM == pow(DS, o_k[1], o_k[0]):
        return True
    else:
        return False

def send(Alice_k, Bob_o, DM):
    emsg = enc (DM, Bob_o)
    print ('\n Text is encrypted. emsg=%s'% hex(emsg))
    digsA = dig_s(DM, Alice_k[1][0], Alice_k[1][2])
    print('\n Message was signed with a secret key of Alice. \n digsA=%s'% hex(digsA))
    digsA1 = enc(digsA, Bob_o)
    print('\n Sign of Alice was signed with open key of Bob. \n digsA1=%s'% hex(digsA1))
    Alice_msg = [emsg,digsA1]
    return Alice_msg

def receive(msg, Bob_s, Alice_o):
    
    decmsg = dec(msg[0], Bob_s)
    print ('\n decmsg is %s'% hex(decmsg))
    decs = dec(msg[1], Bob_s)
    print ('\n decs is %s'% hex(decs))
    print ('\n decs to power e by module n is(sa^emod(n))', hex(pow(decs, Alice_o[1], Alice_o[0])))
    return verify(decs,decmsg,Alice_o)

def site_hex(m):
    return hex(m)[0] + hex(m)[2:]


print('\Choose among: \n1) Site \n2) Py')
choice = input()

if int(choice)==1:
    print("\nGenerating a pair p and q for Alice:\n")
    pq=mass_gen(256)
    Alice_k=keygen(pq)
    msg=random.randint(0,Alice_k[0][0]-1)
    print('\nAn open key (n=%s, e=%s) and secret key (d=%s, pq=%s, %s) for Alice were generated.'% (hex(Alice_k[0][0]),hex(Alice_k[0][1]),hex(Alice_k[1][0]),hex(Alice_k[1][1][0]),hex(Alice_k[1][1][1])))
    print('\nAlice generated a secret message \'%s\' for Bob.'% hex(msg))

str_req = f"http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize=512"
keygen_req = requests.get(str_req)
print("API public key:" + str(keygen_req.json()))
nBob = int(keygen_req.json()["modulus"], 16)
eBob = int(keygen_req.json()["publicExponent"], 16)
    
Bob_o=[nBob,eBob]
print('\nSite has generated an open key (n=%s, e=%s) for Bob)'% (Bob_o[0],Bob_o[1]))

message = send(Alice_k,Bob_o,msg)
kluch1, signatura1 = message

str_request = f"http://asymcryptwebservice.appspot.com/rsa/receiveKey?key={site_hex(kluch1)}&signature={site_hex(signatura1)}&modulus={site_hex(Alice_k[0][0])}&publicExponent={site_hex(Alice_k[0][1])}"

keygen_req = requests.get(str_request, cookies=keygen_req.cookies)
print("Answer: " + str(keygen_req.json()))


if int(choice)==2:
    pq=[]
    for k in range(0,2,1):
        if k==0: 
            print("\nGenerating a pair p and q for Alice:\n")
            pair=mass_gen(256)
            pq.append(pair)
            print("\nPair p and q for Alice:%s, %s"% (hex(pq[0][0]),hex(pq[0][1])))
            
        if k==1: 
            print("\nGenerating a pair p and q for Bob:\n")
            pair=mass_gen(256)
            pq.append(pair)
            while pq[0][0]*pq[0][1]>=pq[1][0]*pq[1][1]:
                pair=mass_gen(256)
                pq.pop(1)
                pq.append(pair)
            print("\nPair p and q for Bob:%s, %s"% (hex(pq[1][0]),hex(pq[1][1])))

    Alice_k=keygen(pq[0])
    Bob_k=keygen(pq[1])
    while Bob_k[0][0]<Alice_k[0][0]:
        Alice_k=keygen(pq[0])

    print('\n Open key (n=%s, e=%s) and secret key (\nd=%s, \npq=%s, \n%s) for Alice.'% (hex(Alice_k[0][0]),hex(Alice_k[0][1]),hex(Alice_k[1][0]),hex(Alice_k[1][1][0]),hex(Alice_k[1][1][1])))
    print('\nOpen key (n=%s, e=%s) and secret key (\nd=%s, \npq=%s, \n%s) for Bob.\n'% (hex(Bob_k[0][0]),hex(Bob_k[0][1]),hex(Bob_k[1][0]),hex(Bob_k[1][1][0]), hex(Bob_k[1][1][0])))

    msg=random.randint(0,Alice_k[0][0]-1)
    
    print('Alice`s  secret message \'%s\' for Bob.'% hex(msg))

    Alice_msg=send(Alice_k,Bob_k[0],msg)
    if receive(Alice_msg,Bob_k[1],Alice_k[0])==True: print('\Work done')
    else: print('\n Failed')
    



















    














          
            
            

import random
import math


def isPseudoPrime(p):
    print(p)
    s = 1
    while (p - 1) % (2 ** s) == 0:
        s += 1
    s -= 1
    d = (p - 1) // (2 ** s)

    #print(p, s, d)
    counter = 0
    errMessage = 0

    for x in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}:
       if p % x != 0 and counter != -1:

           if pow(x, d, p) == 1 or pow(x, d, p) == p - 1:
               counter += 1
       
           for r in range (1, s):
               xr = pow(x, d * pow(2, r), p)

               if xr == p - 1:
                   counter += 1
                   break
               if xr == 1:
                   counter = -1
                   break
       if counter == -1:
           print("xr = 1")
           errMessage = 1
           break
       if p % x == 0:
           print("This p is divisible by", x)
           errMessage = 1
           break

    if counter < 15:
        if errMessage == 0:
            print("counter < 15")
        return 0
    else:
        return 1


def GeneratePrimeNumber(lenmin, lenmax):
    p = random.randrange(2 ** lenmin, 2 ** lenmax)

    while p % 2 == 0:
        p = random.randrange(2 ** lenmin, 2 ** lenmax)

    if isPseudoPrime(p) == 0:
        p = GeneratePrimeNumber(lenmin, lenmax)
    else:
        print(p, "is pseudoprime!")
    return p


def evklid(a, n):
    if math.gcd(a, n) > 1:
        return None
    r = [n, a]
    q = [1]
    v = [0, 1]

    print(n, a)
    i = 1

    while (r[i - 1] % r[i]) != 0:
        q.append(r[i - 1] // r[i])
        r.append(r[i - 1] % r[i])
        v.append(v[i - 1] - v[i] * q[i])
        #print(r[i], q[i], r[i+1], v[i+1])
        i += 1

    vi = v[i] % n
    return vi


def GenerateKeyPair():
    p_ = GeneratePrimeNumber(256, 257)
    q_ = GeneratePrimeNumber(256, 257)
    p1_ = GeneratePrimeNumber(256, 257)
    q1_ = GeneratePrimeNumber(256, 257)

    print("\n\nGenerating good p and q:")
    
    i = 1
    while isPseudoPrime(2 * i * p_ + 1) == 0:
        i += 1
    p = 2 * i * p_ + 1
    print("\n", i, p, "\n\n")

    i = 1
    while isPseudoPrime(2 * i * q_ + 1) == 0:
        i += 1
    q = 2 * i * q_ + 1
    print("\n", i, q, "\n\n")

    i = 1
    while isPseudoPrime(2 * i * p1_ + 1) == 0:
        i += 1
    p1 = 2 * i * p1_ + 1
    print("\n", i, p1, "\n\n")

    i = 1
    while isPseudoPrime(2 * i * q1_ + 1) == 0:
        i += 1
    q1 = 2 * i * q1_ + 1
    print("\n", i, q1, "\n\n")
    
    #print(p, q, p1, q1, "\n\n")

    if p > p1:
        temp = p
        p = p1
        p1 = temp
    if q > q1:
        temp = q
        q = q1
        q1 = temp

    print("p:", p)
    print("q:", q)
    print("p1:", p1)
    print("q1:", q1, "\n\n")

    e = 65537
    e1 = 65537
    n = p * q
    n1 = p1 * q1

    Fn = (p - 1) * (q - 1)
    Fn1 = (p1 - 1) * (q1 - 1)

    d = evklid(e, Fn)
    d1 = evklid(e1, Fn1)

    public_key_A = [e, n]
    public_key_B = [e1, n1]

    private_key_A = d
    private_key_B = d1

    print("A has public key:", public_key_A[0], public_key_A[1])
    print("A has private key:", private_key_A)
    print("B has public key:", public_key_B[0], public_key_B[1])
    print("B has private key:", private_key_B)

    return [public_key_A, private_key_A, public_key_B, private_key_B]

def GenerateMessage(public_key):
    M = random.randrange(0, public_key[1])
    return M

def Encrypt(M, public_key):
    C = pow(M, public_key[0], public_key[1])
    return C

def Decrypt(C, private_key, public_key):
    M = pow(C, private_key, public_key[1])
    return M

def Sign(M, private_key, public_key):
    S = pow(M, private_key, public_key[1])
    return [M, S]

def Verify(SignedM, public_key):
    if SignedM[0] == pow(SignedM[1], public_key[0], public_key[1]):
        return 1
    else:
        return 0


def SendKey(k, private_key, public_key, public_key1):
    S = pow(k, private_key, public_key[1])
    S1 = pow(S, public_key1[0], public_key1[1])
    k1 = pow(k, public_key1[0], public_key1[1])
    return [k1, S1]

def ReceiveKey(SendedKey, private_key1, public_key, public_key1):
    k = pow(SendedKey[0], private_key1, public_key1[1])
    S = pow(SendedKey[1], private_key1, public_key1[1])

    print("k:", k)
    print("S:", S)
    print("Sign checking:", pow(S, public_key[0], public_key[1]))

    if k == pow(S, public_key[0], public_key[1]):
        return 1
    else:
        return 0

#print(evklid(12, 20))

[pub_keyA, priv_keyA, pub_keyB, priv_keyB] = GenerateKeyPair()

print("\n\nChecking of encrypting and decrypting:")
print("pub_keyA:", pub_keyA)
print("priv_keyA:", priv_keyA)
print("pub_keyB:", pub_keyB)
print("priv_keyB:", priv_keyB)

M = GenerateMessage(pub_keyA)
C = Encrypt(M, pub_keyA)
print("\n\nM:", M)
print("C:", C)
print("Decrypted message:", Decrypt(C, priv_keyA, pub_keyA))
if M == Decrypt(C, priv_keyA, pub_keyA):
    print("A decrypts message from B successfully")
else:
    print("A can`t decrypt message from B")

M1 = GenerateMessage(pub_keyB)
C1 = Encrypt(M1, pub_keyB)
print("\n\nM1:", M1)
print("C1:", C1)
print("Decrypted message:", Decrypt(C1, priv_keyB, pub_keyB))
if M1 == Decrypt(C1, priv_keyB, pub_keyB):
    print("B decrypts message from A successfully")
else:
    print("B can`t decrypt message from A")


print("\n\nChecking of signing and verifying:")
SignedM = Sign(M, priv_keyA, pub_keyA)
print("\n\nS:", SignedM[1])
if Verify(SignedM, pub_keyA) == 1:
    print("A was verified successfully")
else:
    print("A wasn`t verified")

SignedM1 = Sign(M1, priv_keyB, pub_keyB)
print("\n\nS1:", SignedM1[1])
if Verify(SignedM1, pub_keyB) == 1:
    print("B was verified successfully")
else:
    print("B wasn`t verified")


k = GenerateMessage(pub_keyA)
print("\n\nUsing of protocol of key distribution:")

if pub_keyA[1] <= pub_keyB[1]:
    SendedKey = SendKey(k, priv_keyA, pub_keyA, pub_keyB)
    print("\n\nA sended key:", SendedKey)

    if ReceiveKey(SendedKey, priv_keyB, pub_keyA, pub_keyB) == 1:
        print("A was authenticated successfully")
    else:
        print("A wasn`t authenticated")

else:
    SendedKey = SendKey(k, priv_keyB, pub_keyB, pub_keyA)
    print("\n\nB sended key:", SendedKey)

    if ReceiveKey(SendedKey, priv_keyA, pub_keyB, pub_keyA) == 1:
        print("B was authenticated successfully")
    else:
        print("B wasn`t authenticated")


print("\n\n\nInteraction with site:")
k = GenerateMessage(pub_keyA)
print("k:", hex(k))
print("\nA has public key:", hex(pub_keyA[0]), hex(pub_keyA[1]))
print("and private key:", hex(priv_keyA))
pub_keyB[1] = 0xD8B37B1B013D8E7A63B526AA99C00DB8BBBB56AC38F5CB3D5A2B55C2CEBED8C24327866639C1601B0169D2473B9BA662CB6C960D96A989D177EF99B53B21D16961A7357225CDF3182411D7
print("\nSite has key:", hex(pub_keyB[1]))
pub_keyB[1] = int(pub_keyB[1])

SendedKey = SendKey(k, priv_keyA, pub_keyA, pub_keyB)
print("\nA sended key:", SendedKey)
print("k1:", SendedKey[0])
print("S1:", SendedKey[1])
print("k1 in hex notation:", hex(SendedKey[0]))
print("S1 in hex notation:", hex(SendedKey[1]))
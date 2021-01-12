import random

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def euclid(a, b): #роширений алгоритм евкліда
    if (b == 0):
        return a, 1, 0
    d, x, y = euclid(b, a % b)
    return d, y, x - (a // b) * y

def ober(b, n):
    g, x, y = euclid(b, n)
    if g == 1:
        return x % n

def MilleraRabina(n, k):
    t = 0
    m = n - 1
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    while m % 2 == 0:
        m = m // 2
        t += 1
    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, m, n)
        if x == 1 or x == n - 1:
            continue
        j = 1
        while x != -1 and j < t:
            x = pow(x, 2, n)
            if x == n - 1:
                break
            j = j + 1
        else:
            return False
    return True

def GenerateKeyPair(n):

    pq = []
    e = 2 ** 16 + 1
    while len(pq) != 2:
        a = random.getrandbits(n-1) + (1 << n-1)
        if not MilleraRabina(a, 10):
            back = False
            while back is False:
                a = random.getrandbits(n - 1) + (1 << n - 1)
                if MilleraRabina(a, 10):
                    pq.append(a)
                    back = True
    n = pq[0] * pq[1]
    public_key = [e, n]
    fi = (pq[0] - 1) * (pq[1] - 1)
    private_key = ober(e, fi)
    return public_key, private_key

def Encrypt(M, publickey):
    C = pow(M, publickey[0], publickey[1])
    return C

def Decrypt(C, private_key, public_key):
    M = pow(C, private_key, public_key)
    return M

def Sign(M, private_key, public_key):
    signature = pow(M, private_key, public_key[1])
    S = [M, signature]
    return S

def Verify(KS, publickey):
    message = pow(KS[1], publickey[0], publickey[1])
    if KS[0] == message:
        return True
    else:
        return False

def SendKey(M, privatkeyA, publickeyA, publickeyB):
    S = Decrypt(M, privatkeyA, publickeyA[1])
    S1 = Encrypt(S, publickeyB)
    k1 = Encrypt(M, publickeyB)
    return [k1, S1]

def ReceiveKey(privatekeyB, publickeyB, publickeyA, KS):

    k = Decrypt(KS[0], privatekeyB, publickeyB[1])
    s = Decrypt(KS[1], privatekeyB, publickeyB[1])
    ks = [k, s]
    if Verify(ks, publickeyA) is True:
        return ks[0]
    else:
        return False


if __name__ == "__main__":

    public_keyA, private_keyA = GenerateKeyPair(256)
    public_keyB, private_keyB = GenerateKeyPair(256)

    while public_keyA[1] > public_keyB[1]:
        public_keyB, private_keyB = GenerateKeyPair(256)

    text = 234567
    # C = Encrypt(text, public_keyA)
    # M = Decrypt(C, private_keyA, public_keyA)
    # print(M)

    ks = SendKey(text, private_keyA, public_keyA, public_keyB)
    print(ks)
    print(ReceiveKey(private_keyB, public_keyB, public_keyA, ks))
    #################################
    n1 = int('9436B74E95CC6EB2FDFF568915C66099E0BFA07E1F9E35324C16AD87A40334F4EAD96CFE84001721B35906E6B99C43DB2F3C46860CC4A6AE010EA57B179298C9', 16)

    public_keyB[1] = n1
    ks2 = SendKey(text, private_keyA, public_keyA, public_keyB)

    print(hex(ks2[0]))
    print(hex(ks2[1]))
    print(hex(public_keyA[1]))
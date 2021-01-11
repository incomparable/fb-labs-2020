import math, random, requests


def num_gen(lim1, lim2):
    return random.randint(lim1,lim2)



def egcd(a,b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y ,x = egcd(b%a, a)
        return (g, x - (b//a)*y, y)


def miller_rabin_test(n):
    k = 100
    d = n - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d = d // 2

    for i in range(k):
        x = num_gen(2, n - 1)
        if math.gcd(x, n) > 1:
            return False
        x = pow(x, d, n)
        if x == 1 or x == (n - 1):
            continue
        else:
            p_prime = False

            for m in range(1, s):
                x_r = x * pow(x, 2 ** m, n)
                if x_r == n - 1:
                    p_prime = True
                elif x_r == 1:
                    return False
            if not p_prime:

                return False
    return True


def inverse(a, b):
    g, x, y = egcd(a, b)
    if g == 1:
        return x % b
    else:
        return False


def prime_gen(bit):
    min = 1 << bit # to get "100...000"
    max = (1 << bit + 1) - 1 # to get "1111...1111"
    r_n = num_gen(min, max)
    while True:
        if r_n % 2 == 0: # isn`t prime
            r_n += 1
        elif miller_rabin_test(r_n):
            print('2')
            break
        else:
            print(r_n ,'Is not a prime number.')
            r_n +=2
    return r_n


def key_generator(bit):
    e = 0
    p = prime_gen(bit)
    q = prime_gen(bit)
    print('1')
    while p == q:
        q = prime_gen(bit)
    n = p*q
    euler_n = (p-1)*(q-1)
    while math.gcd(e, euler_n) != 1:
        e = num_gen(2, euler_n - 1)
    d = inverse(e,euler_n)
    if d < 0:
        d = d + euler_n #mod
    open_key = [e,n]
    secret_key = [d,n]
    return [open_key, secret_key]


def enc(msg, open_key):
    return pow(msg,open_key[0], open_key[1]) #msg^emod(n)


def dec(enc_msg, secret_key):
    return pow(enc_msg, secret_key[0], secret_key[1]) #enc_msg^dmod(n)


def sign(msg, secret_key):
    signature = enc(msg, secret_key)
    return signature


def verification(sign, msg, open_key):
    if msg == pow(sign, open_key[0], open_key[1]):
        return True
    else:
        return False


def send(k, A_secret_key, B_open_key):
    k1 = enc(k,B_open_key)
    S = sign(k,A_secret_key)
    print ('Signature is: ', S)
    S1 = enc(S,B_open_key)
    secret_msg = [k1,S1]
    return secret_msg


def receive(secret_msg, A_open_key, B_secret_key):
    k = dec (secret_msg[0], B_secret_key)
    S = dec (secret_msg[1], B_secret_key)
    print('Starting to receive a key')
    print('The key is: ', k)
    print('Signature is: ', S)
    return verification(S,k,A_open_key)


def s_hex(m):
    return hex(m)[0] + hex(m)[2:]

print('\Choose among: \n1) Site \n2) Py')
choice = input()

if int(choice) == 1:

    print ('Generating key pair for Alice:')
    A = key_generator(255)
    print ('Public exponent (e) is %s' % hex (A[0][0]))
    print ('Private key (d) is %s:' % hex (A[1][0]))
    print ('Modulus is (n) is %s' % hex (A[0][1]))
    msg = 123
    print ('Secret message was generated: %s' % hex(msg))

    str_req = f"http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize=512"
    keygen_req = requests.get(str_req)
    print("API public key:" + str(keygen_req.json()))
    site_n = int(keygen_req.json()["modulus"], 16)
    site_e = int(keygen_req.json()["publicExponent"], 16)

    site_open = [site_e, site_n]
    print('\nSite has generated an open key (e=%s, n=%s) for Bob)' % (site_open[0], site_open[1]))

    message = send(msg,A[1],site_open)
    k1, s1 = message
    print(k1)
    print(hex(k1))
    print(s_hex(k1))
    str_request = f"http://asymcryptwebservice.appspot.com/rsa/receiveKey?key={s_hex(k1)}&signature={s_hex(s1)}&modulus={s_hex(A[0][1])}&publicExponent={s_hex(A[0][0])}"
    keygen_req = requests.get(str_request, cookies=keygen_req.cookies)
    print("Answer: " + str(keygen_req.json()))

if int(choice) == 2:
    print('Generating key pair for Alice:')
    A = key_generator(256)
    print('Public exponent (e) is %s' % hex(A[0][0]))
    print('Private key (d) is %s:' % hex(A[1][0]))
    print('Modulus is (n) is %s' % hex(A[0][1]))
    print('Generating key pair for Bob:')
    B = key_generator(257)
    print('Public exponent (e) is %s' % hex(B[0][0]))
    print('Private key (d) is %s:' % hex(B[1][0]))
    print('Modulus is (n) is %s' % hex(B[0][1]))
    l = num_gen(1,100000)
    print('Secret message is now ', l)
    enc_l = enc(l, A[0])
    print('Encrypted message L is: ', enc_l)
    dec_l = dec(enc_l, A[1])
    print('Decrypted back message is ', dec_l )
    print('Lets see how Send and Receive works: ')
    k = 124
    print('Shared key is: ', k)
    msg = send (k, A[1], B[0])
    print('Encrypted signature: ', msg[1])
    print('Encrypted message: ', msg[0])
    if receive(msg,A[0],B[1]):
        print('The key was successfully received')
    else:
        print('Something went wrong')







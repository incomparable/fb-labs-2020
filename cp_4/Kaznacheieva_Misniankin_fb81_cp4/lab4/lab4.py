from random import randint


def gcd (first, second): # використаємо алгоритм пошуку НСД з 3 лабораторної роботи
    if second != 0:
        return gcd(second, first % second)
    else:
        return first

def gcd1 (first, second):
    if first == 0:
        return (second, 0, 1)
    else:
        g, x, y = gcd1(second % first, first)
        return (g, y - (second // first) * x, x)
    

def inv(first, second):
    g, x, _ = gcd1(first, second)
    if g == 1:
       # print (x % second)
        return x % second
    else: 
        #print ('no')
        return 1

def generator(length):
    prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97] #простые числа до 100
    min = pow(2, length)
    max = pow(2, length+1) - 1
    random_num = randint(min, max)
    while True:
        for rand in prime_nums:
            if random_num % rand == 0:
                random_num += 1
                break
            elif rand==97 and random_num%rand!=0:
                #print(random_num)
                return random_num
def mil_rab_test(n):
    k = 95
    S = 0 
    d = n - 1
    pseudopr = False
    while d%2 == 0:
        S +=1
        d = d //2
    for i in range(k):
        x = randint(2, n-1)
        if gcd(x, n) > 1:
            return False
        x_1 = pow(x, d, n)
        if x_1 == 1 or x_1 == n - 1:
            continue
        else:
            for l in range(1,S):
                m = pow(2,l)
                x_r = pow(x_1,l,n)
                if x_r == n - 1:
                    return True
                else:
                    return False
            if not pseudopr:
                return False
    return True

def gen_num(length):
    while True:
        x = generator(length)
        if mil_rab_test(x):
            #print ('The num is prime ' + str((x)))
            break
        else:
            x+=2
            #print ('The num is not prime ' + str((x)))
            continue
    return x

def key_pair(length) :
   # print('p:')
    p = gen_num(length)
    #print('q:')
    q = gen_num(length)
    if p == q:
        q = gen_num(length)
    n = q*p
    oiler = (q - 1)*(p - 1)
    e = randint(2,(oiler-1))
    while gcd(e,oiler)!=1:
            e = randint(2,(oiler-1))
    d = inv(e,oiler)
    pr_key = [e,n]
    pub_key = [d,n]
    #print('Keys were generated!')
    return [pr_key, pub_key]

def encrypt(message, pub_key):
    encr = pow(message,pub_key[0],pub_key[1])
    return encr

def decrypt(mess, pr_key):
    decr = pow(mess,pr_key[0],pr_key[1])
    return decr

def signature(message, pr_key):
    sign = encrypt(message, pr_key)
    return sign

def verify(message, sign, pub_key):
    if message == encrypt(sign, pub_key):
        return True
    else:
        return False

def SendKey(key,pr_keyA,pub_keyB):
    key_1 = encrypt(key,pub_keyB)
    Si = signature(key,pr_keyA)
    Sign=encrypt(Si,pub_keyB)
    return [key_1,Sign]

def ReceiveKey(Al_mess, pr_keyB, pub_keyA):
    key = Al_mess[0]
    Sign = Al_mess[1]
    message = decrypt(key,pr_keyB)
    sign = decrypt(Sign,pr_keyB)
    if verify(message, sign, pub_keyA):
        return k
    else:
        return None



print('Alice:')
keys_1 = key_pair(255)
print('Keys for Alice:\nPrivate:')
print(keys_1[0][0])
print('Public:')
print(keys_1[1][0])
print('\nBob:')
keys_2 = key_pair(255)
print('Keys for Bob:\nPrivate:')
print(keys_2[0][0])
print('Public:')
print(keys_2[1][0])
print()
print()
print('Let`s encrypt and decrypt some message with Alice`s keys:')
message=gen_num(255)
print('Message:'+str(message))
encr_mess= encrypt(message,keys_1[0])
print('Encrypted message:'+str(encr_mess))
decr_mess = decrypt(encr_mess,keys_1[1])
print('Decrypted message:'+str(decr_mess))
print()
print('Let`s encrypt and decrypt some message with Bob`s keys:')
message=gen_num(255)
print('Message:'+str(message))
encr_mess= encrypt(message,keys_2[0])
print('Encrypted message:'+str(encr_mess))
decr_mess = decrypt(encr_mess,keys_2[1])
print('Decrypted message:'+str(decr_mess))
print()
print()
print('Digital signature with Alice private key:')
sign = signature(message, keys_1[0])
print('Signature:' + str(sign))
yesno = verify(message, sign, keys_1[1])
print('It was from Alice? '+ str(yesno))
print()
print()
print('Send Key, Receive Key prot:')
k = gen_num(255)
print('We shared this key: ' +str(k))
messA=SendKey(k,keys_1[0],keys_2[1])
print('What we have after encryption:' +str(messA[0]))
print('Signature:' +str(messA[1]))
k = ReceiveKey(messA,keys_2[0], keys_1[1])
print('Key:' + str(k))
print()
print()
print('On server we get:')
modulus=int('65D35726E3C0B92464B811160CE5D21BE262A4B2634CD3496810C43BD8EA424F',16)
exp = int("10001",16)
print('Server public key: '+ str(exp))
print('Server modulus: ' + str(modulus))
print()
print()
messA = gen_num(255)
serv = [exp,modulus]
f_serv = SendKey(messA, keys_1[1], serv)

print('Encrypted message from server: ' + str(f_serv))
print('Signature from server: ' + str(f_serv))
first = hex(f_serv[0])[-1]
second = hex(f_serv[1])[-1]
third = hex(keys_1[1][1])[-1]
fourth = hex(keys_1[1][0])[-1]
URL = 'http://asymcryptwebservice.appspot.com/rsa/receiveKey?key={}&signature={}&modulus={}&publicExponent={}'.format(first, second, third, fourth)
print(URL)
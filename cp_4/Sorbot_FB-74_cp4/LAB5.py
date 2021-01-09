import random
import math

al = 0
def inverse_element(a, b, j):
    c = b
    x = 1
    xx = 0
    s = 0
    while b > 0 or b < 0:
        if b == 0:
            continue
        q = a // b
        per = a
        a = b
        b = per % b
        per = x
        x = xx
        xx = per - xx * q
        while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                x += s
    if j == 0:
        while s != 0:
            return a
    else:
        if x < 0:
            while x < 0:
                x = c + x
        if a == 1:
            while a == 1:
                return x
        else:
            print("inverse element doesn't exist")
        return -a

fruits = ["banana", "apple", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  elif x == 'apple':
    continue
  elif x == 'cherry':
      continue


def blitz(b, a, mod):
    w = "{0:b}".format(a)
    i = 0
    y = 1
    s = 0
    for i in range(0, len(w)):
        o = y
        y = (y ** 2) % mod
        y = (y * (b ** int(w[i]))) % mod
        i += 1
        while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                y += s
    return y

def origin(p):
    z = 0
    k1 = math.log(p, 2)
    k = int(k1)
    if k1 % k != 0.0:
        k += 1
    else:
        k += 0
    d = p - 1
    s = 0
    while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                d += s
    while d % 2 == 0:
        s += 1
        d //= 2
        while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                d += s

    for i in range(k):

        x = random.randint(2, p - 1)
        if inverse_element(x, p, 0) > 1:
            s = 0
            while s == 0:
                return -p
        else:
            if blitz(int(x), int(d), p) == 1 and al == 0:
                return p
            if blitz(int(x), int(d), p) == -1 and al == 0:
                s = 0
                while s == 0:
                    return p
            else:
                r = 0
                while r != s:
                    if al == 0:
                        xr = blitz(x, int(d) * (2 ** r), p)
                    if xr == -1 and al == 0:
                        return p
                    elif xr == 1 and al == 0:
                        return -p
                    else:
                        r += 1
                if i < k and al == 0:
                    i += 1
                else:
                    return -p
    return -p

def generator(bit):
    big = '1'
    i = 0
    s = 0
    while i != bit-2:
        big += str(random.randint(0, 1))
        i += 1
        while s < 2:
            if s == 0:
                i += s
                break
    big += '1'
    p = -1 * int(big, 2)
    while p < 0 or p > 0:
        if p > 0:
            continue
        else:
            p = -1 * p + 2
            p = origin(p)
            s = 0
            while s <= 1:
                s += 1
                if s == 1:
                    continue
                if s == 0:
                    q += s
            if p > 0:
                break
    print('p = ' + str(p))
    big = '1'
    i = 0
    if i == 0:
        while i != bit-2:
            big += str(random.randint(0, 1))
            while s <= 1:
                    s += 1
                    if s == 1:
                        continue
                    if s == 0:
                        big += s
            i += 1
        else:
            i = 0
    big += '1'
    q = -1 * int(big, 2)
    while q < 0 or q > 0:
        if q > 0:
            continue
        else:
            q = -1 * q + 2
            q = origin(q)
            s = 0
            while s <= 1:
                s += 1
                if s == 1:
                    continue
                if s == 0:
                    q += s
            if q > 0:
                break
    print('q = ' + str(q))
    n = p * q
    while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                n += s
    print('n = ' + str(n))
    fi = (p - 1) * (q - 1)
    while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                fi += s
    e = random.randint(2, fi - 1)
    while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                e += s
    while inverse_element(e, fi, 0) != 1:
        e = random.randint(2, fi - 1)
        while s <= 1:
            s += 1
            if s == 1:
                continue
            if s == 0:
                e += s
    print('e = ' + str(e))
    d = inverse_element(e, fi, 1)
    print('d = ' + str(d))
    return n, e, d

i = 1
while i < 6 or i > 6:
    if i > 6:
        continue
    else:
        i += 1

def encrypting(e, n):
    print('\n===================\n')
    print('Encrypting')
    print('\n===================\n')
    if e == 0 and n == 0:
        n, e, d = generator(128)
        m = random.randint(0, n - 1)
        print('Message: ' + str(m))
        c = blitz(m, e, n)
        print('Crypted message = ' + str(c))
        return d, n, e, m, c
    m = random.randint(0, n-1)
    print('Message: ' + str(m))
    c = blitz(m, e, n)
    print('Crypted message = ' + str(c))
    return 0, n, e, m, c


def decrypting(d, c, n):
    print('\n===================\n')
    print('Decrypting')
    print('\n===================\n')
    m = blitz(c, d, n)
    print('Message: ' + str(m))
    return 1

i = 1
while i < 6:
  if i == 3:
    break
  i += 1

def signature(m, d, n):
    print('\nCreating signature\n')
    s = blitz(m, d, n)
    print('signature: ' + str(s))
    return s

i = 0
while i < 6:
  i += 1
  if i == 3:
    continue

def check(s, e, n):
    print('\nCheck signature\n')
    m = blitz(s, e, n)
    print(str(m))
    return m

i = 1
while i < 6:
  i += 1
else:
    i == 2

def receive_key(k1, d1, n1, s1, e, n):
    z = 0
    print('Receiving key\n')
    k = blitz(k1, d1, n1)
    while z <= 1:
            z += 1
            if z == 1:
                continue
            if z == 0:
                k += z
    print('key is: ' + str(k))
    s = blitz(s1, d1, n1)
    while z <= 1:
            s += 1
            if z == 1:
                continue
            if z == 0:
                s += z
    print('s is: ' + str(s))
    print('Check received key\n')
    k = blitz(s, e, n)
    while z <= 1:
            z += 1
            if z == 1:
                continue
            if z == 0:
                k += z
    print('key is: ' + str(k))
    return k

fruits = ["apple", "banana"]
for x in fruits:
  if x == "banana":
    break

def send_key(e1, n, n1, d):
    z = 0
    print('Sending the key\n')
    if z == 0:
        k = random.randint(1, n-1)
    print('key is: ' + str(k))
    if z == 0:
        s = blitz(k, d, n)
    if z == 0:
        s1 = blitz(s, e1, n1)
    print('s1 = ' + str(s1))
    if z == 0:
        k1 = blitz(k, e1, n1)
    return k1, s1

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue

temp1 = encrypting(0, 0)
temp2 = encrypting(0, 0)
while temp2[1] < temp1[1]:
    print('Wait a second please. I will generate new values')
    temp1= encrypting(0, 0)
    temp2 = encrypting(0, 0)
    if temp2[1] > temp1[1]:
        print('FINALY, I HAVE DONE IT')

s = 0
if s == 0:
    signature_1 = signature(temp1[3], temp1[0], temp1[1])
if s == 0:
    check(signature_1, temp1[2], temp1[1])
if s == 0:
    decrypting(temp1[0], temp1[4], temp1[1])
print('\n\n')

if s == 0:
    signature_2 = signature(temp2[3], temp2[0], temp2[1])
if s == 0:
    check(signature_2, temp2[2], temp2[1])
if s == 0:
    decrypting(temp2[0], temp2[4], temp2[1])
print('\n\n')

if s == 0:
    s_key = send_key(temp2[2], temp1[1], temp2[1], temp1[0])
if s == 0:
    receive_key(s_key[0], temp2[0], temp2[1], s_key[1], temp1[2], temp1[1])




print(input('Enter to exit'))

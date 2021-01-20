from collections import Counter
import re
import array

alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ')

most_used_bigr = ('ст', 'но', 'то', 'на')

def ord(letter):
    if letter in alpha:
        #print(alpha.index(letter))
        return alpha.index(letter)
def chr(index):
    if index < len(alpha):
        #print(alpha[index])
        return alpha[index]

def count_bigr(filename): #cчитаем биграммы и выводим топ 5 
    fin = open (filename, 'rt', encoding='utf-8')
    text = fin.read().replace('\n', '')
    s = re.findall(r'(?=([а-я]{2}))', text)
    t = Counter(s)
    l = list()
    for bgr in s:
        t[bgr]+=1
    t.most_common(5)
    p = t.most_common(5)
    print (p)
    l.extend(p)
    return l


def crack(x1,x2,y1,y2):
    #y' = (a*x' + b) (mod m^2)
    #y'' = (a*x'' + b) (mod m^2)
    # y' - y'' = a(x'-x'') mod m^2
    # x' - наиболее частая биграмма в языке, х'' -следующая за ней по частоте, аналогично с у' и y'' (только в тексте)
    rb1 = (ord(x1[0]))*31+ord(x1[1])
    rb2 = (ord(x2[0]))*31+(ord(x2[1]))
    cb1 = (ord(y1[0]))*31+(ord(y1[1]))
    cb2 = (ord(y2[0]))*31+(ord(y2[1]))
    #print(rb1, rb2, cb1, cb2)
    n1 = (rb1 - rb2)% (31*31)#a
    n2 = (cb1 - cb2)% (31*31)#b
    n = 31*31
    d=gcd(n1,n)
    if d == 1:
        a = (inv(n1, n) * n2) % n
        key= [a, (cb1-a*rb1) % n]
        #print(key)
        return key
    if d > 1:
        if n2 % d != 0:
            return 0
        if n2 % d == 0:
            n3 = n2/d
            while 1:
                if(n2 % n1 == 0):
                    x = n2 / n1
                    break
                n2 += n3
            keys=[]
            for i in range(d):
                x_0 = x + n3*i
                x_1 = (cb1-((x + n3*d)*rb1)) % n
                key=[x_0, x_1]
                keys.append(key)

        #print(keys)
        return keys
   
   
    

def f(l): #массив без повторений
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n
   
def find_key(file): # a = key1, b=key2, n=31
    fin=open(file,'rt', encoding='utf-8')
    text=fin.read()
    temp = ''
    t = count_bigr(file)
    most_used_bigr = ('ст', 'но', 'то', 'на')
    t = [t[0][0], t[1][0], t[2][0], t[3][0]]
    #print(t)
    new_text = ''
    lst = list()
    for i in most_used_bigr:
        for j in most_used_bigr:
            for k in t:
                for l in t:
                    if i != j:
                        if k != l:
                            key = crack(i,j,k,l)
                            lst.append(key)
                        else: continue
                    else: continue
    print(f(lst))
def decrypt(filename, key1, key2):
    fin=open(filename,'rt', encoding='utf-8')
    fout= open('result.txt', 'wt', encoding='utf-8')
    text = fin.read().replace('\n', '')
    new_arr = [text[i:i+2] for i in range(0, len(text),2)]
    new_text=''
    for bigr in new_arr:
         first = (((inv(key1, 961) * (( (ord(bigr[0])) * 31) + (ord(bigr[1])) - key2)) % 961) // 31) 
         second = ((inv(key1, 961) * (( (ord(bigr[0])) * 31) + (ord(bigr[1])) - key2)) % 961) % 31 
         new_bigramm = chr(first) + chr(second)
         new_text +=new_bigramm
         fout.write(new_bigramm)
    print(new_text)
    
    


def gcd (first, second):
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


def auto_check(filename):
    alpha1 = ('о', 'а','е','щ','ф','ь')
    let_count = 0
    fin=open(filename,'rt', encoding='utf-8')
    text = fin.read()
    for let in text:
                let_count = let_count + 1 
    temp_count = 0
    for c in alpha1:
        if c == 'o' and text.count(c)*100/let_count < 10:
            break
        if c == 'a' and text.count(c)*100/let_count < 5:
            break
        if c == 'e' and text.count(c)*100/let_count < 5:
            break
        if c == 'ф' and text.count(c)*100/let_count < 1:
            break
        if c == 'щ' and text.count(c)*100/let_count < 1:
            break
        if c == 'ь' and text.count(c)*100/let_count < 1:
            break
        print('This text was decrypted in the right way! Congratulations!')
 






#count_bigr('07.txt')
#ord('я')
#inv(5, 21)
#chr(1)
#find_key('text.txt')
#crack('ст','но', 'лл', 'цл')
#decrypt ('text.txt', 200, 900)
#inv (12, 5)
#auto_check('result.txt')


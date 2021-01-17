from collections import Counter
import re
import array

alpha = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ')

most_used_bigr = ('ст', 'но', 'то', 'на')


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


def ord(let):
    if let == 'а': return 0
    if let == 'б': return 1
    if let == 'в': return 2
    if let == 'г': return 3
    if let == 'д': return 4
    if let == 'е': return 5
    if let == 'ж': return 6
    if let == 'з': return 7
    if let == 'и': return 8
    if let == 'й': return 9
    if let == 'к': return 10
    if let == 'л': return 11
    if let == 'м': return 12
    if let == 'н': return 13
    if let == 'о': return 14
    if let == 'п': return 15
    if let == 'р': return 16
    if let == 'с': return 17
    if let == 'т': return 18
    if let == 'у': return 19
    if let == 'ф': return 20
    if let == 'х': return 21
    if let == 'ц': return 22
    if let == 'ч': return 23
    if let == 'ш': return 24
    if let == 'щ': return 25
    if let == 'ь': return 26
    if let == 'ы': return 27
    if let == 'э': return 28
    if let == 'ю': return 29
    if let == 'я': return 30

def chr (num):
    if num == 0: return 'а'
    if num == 1: return 'б' 
    if num == 2: return 'в'
    if num == 3: return 'г' 
    if num == 4: return 'д' 
    if num == 5: return 'е' 
    if num == 6: return 'ж' 
    if num == 7: return 'з' 
    if num == 8: return 'и'
    if num == 9: return 'й' 
    if num == 10: return 'к' 
    if num == 11: return 'л' 
    if num == 12: return 'м' 
    if num == 13: return 'н' 
    if num == 14: return 'о' 
    if num == 15: return 'п'
    if num == 16: return 'р'
    if num == 17: return 'с'
    if num == 18: return 'т'
    if num == 19: return 'у'
    if num == 20: return 'ф'
    if num == 21: return 'х'
    if num == 22: return 'ц'
    if num == 23: return 'ч'
    if num == 24: return 'ш'
    if num == 25: return 'щ'
    if num == 26: return 'ь'
    if num == 27: return 'ы'
    if num == 28: return 'э'
    if num == 29: return 'ю'
    if num == 30: return 'я'

def crack(x1,x2,y1,y2):
    #y' = (a*x' + b) (mod m^2)
    #y'' = (a*x'' + b) (mod m^2)
    # y' - y'' = a(x'-x'') mod m^2
    # x' - наиболее частая биграмма в языке, х'' -следующая за ней по частоте, аналогично с у' и y'' (только в тексте)
    #rb1 = (ord(x1[0])-1072)*31+(ord(x1[1])-1072)
    #rb2 = (ord(x2[0])-1072)*31+(ord(x2[1])-1072)
    #cb1 = (ord(y1[0])-1072)*31+(ord(y1[1])-1072)
    #cb2 = (ord(y2[0])-1072)*31+(ord(y2[1])-1072)
    rb1 = (ord(x1[0]))*31+ord(x1[1])
    rb2 = (ord(x2[0]))*31+(ord(x2[1]))
    cb1 = (ord(y1[0]))*31+(ord(y1[1]))
    cb2 = (ord(y2[0]))*31+(ord(y2[1]))

    n1 = (rb1 - rb2)% (31*31)
    n2 = (cb1 - cb2)% (31*31)
    d = gcd(n1,(31*31))
    #print(d)
    n3 = n2/d
    invers = inv(n1, (31*31)) #a
    if d == 1:
        key= [invers, (cb1-invers*rb1) % (31*31)]
        print(key)
        return key
    if d!= 1:
        if d > 1:
            return 0
        elif n2 % d == 0:
            while True:
                if(n2 % n1 == 0):
                    x = n2 / n1
                    break
                n2 += n3

            keys=[]
            print('Let`s create array of keys...')
            for i in range(d):
                key=[x + n3*i, (cb1-((x + n3*d)*rb1) % 961)]
                keys.append(key)
            print(keys)
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
                    key = crack(i,j,k,l)
                    lst.append(key)
   #print(f(lst))
def decrypt(filename, key1, key2):
    fin=open(filename,'rt', encoding='utf-8')
    fout= open('result.txt', 'wt', encoding='utf-8')
    text = fin.read().replace('\n', '')
    new_arr = [text[i:i+2] for i in range(0, len(text),2)]
    new_text=''
    for bigr in new_arr:
         first = (((inv(key1, 961) * (( ord(bigr[0]) * 31) + ord(bigr[1]) - key2)) % 961) // 31) 
         second = ((inv(key1, 961) * (( ord(bigr[0]) * 31) + ord(bigr[1]) - key2)) % 961) % 31 
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
    alpha = ('о', 'а','е','щ','ф','ь')
    let_count = 0
    fin=open(filename,'rt', encoding='utf-8')
    text = fin.read()
    for let in text:
                let_count = let_count + 1 
    temp_count = 0
    for c in alpha:
        if c == 'o' and text.count(c)*100*2/let_count < 10:
            break
        if c == 'a' and text.count(c)*100*2/let_count < 5:
            break
        if c == 'e' and text.count(c)*100*2/let_count < 5:
            break
        if c == 'ф' and text.count(c)*100*2/let_count < 1:
            break
        if c == 'щ' and text.count(c)*100*2/let_count < 1:
            break
        if c == 'ь' and text.count(c)*100*2/let_count < 1:
            break
        print('This text was decrypted in the right way! Congratulations!')
 






count_bigr('07.txt')
#inv(5, 21)
#find_key('07.txt')
#crack('ст','но', 'вм', 'мь')
#decrypt ('07.txt', 200, 900)
#inv (12, 5)
auto_check('result.txt')

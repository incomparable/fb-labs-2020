

alpha = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
                   'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']

rus_bigrams = [["с","т"], ["н","o"], ["е","н"], ["т","о"], ["н","а"]]



    


def letter_ordo(str):
    if ord(str) < 1098: 
        str = ord(str) - 1072
    else:
        if ord(str) > 1097:
            str = ord(str) - 1073
    return str
#print(letter_ordo(rus_bigrams[0][0]))

def text_to_bi(text):
    bi = []
    d=len(text)
    if d%2==0:
        for i in range(0,len(text),2):
            x = [text[i]] + [text[i+1]]
            bi.append(x)
        return bi
    else:
        if d%2==1:
            for i in range(0,d-1,2):
                x = [text[i]] + [text[i+1]]
                bi.append(x)
        y = text[d-1]
        bi.append(y)
        return bi

print(text_to_bi('каву'))

def bi_ordo(bi):
   
    ress = []
    if len(bi)%2==0:  
        bi = text_to_bi(bi)
        for i in range (0,len(bi)):
            x = letter_ordo(bi[i][0]) *31 + letter_ordo(bi[i][1])
            ress.append(x)
        return ress
    else:
        if len(bi)%2==1:
            d= len(bi)
            y = letter_ordo(bi[d-1])*31
            bi = text_to_bi(bi)
            for i in range (0,(d-1)//2):
                 x = letter_ordo(bi[i][0]) *31 + letter_ordo(bi[i][1])
                 ress.append(x)
            
            ress.append(y)
        return ress
text = 'каву'
print(bi_ordo(text)[1])


def check(text):
  alpha = 'оеафщь'
  letter_c = 0
  for letter in text:
    letter_c +=1
    for p in alpha:
      j = 0
      if c p == letter:
        j +=1
      if p == 'o' and j*100/letter_c < 7:
        print('freq of o = '+(str(j*100/letter_c) + '\n')
        return 0
      if p == 'a' and j*100/letter_c < 6:
        print('freq of а = '+(str(j*100/letter_c) + '\n')
        return 0
      if p == 'e' and j*100/letter_c < 6:
        print('freq of е = '+(str(j*100/letter_c) + '\n')
        return 0
      if p == 'ф' and j*100/letter_c > 1:
        print('freq of ф = '+(str(j*100/letter_c) + '\n')
        return 0
      if p == 'щ' and j*100/letter_c > 1:
        print('freq of щ = '+(str(j*100/letter_c) + '\n')
        return 0
  print('seems to be correct')
  return 1



def letter_chro(str):
    if str <= 27:
        str = chr(str + 1072)
    else:
        if str > 27:
            str = chr(str + 1073)
    return str
#print(letter_chro(30))

def bi_chro(bi):
    a = letter_chro( (bi - bi%31)//31)
    b = letter_chro(bi - letter_ordo(a)*31)
    return a+b
    
print (bi_chro(417))



def gcd(a,b):
    d = 0
    if (b == 0):
        return  a
    return gcd(b, a%b)

def exp_euc(a,b):
    if b == 0: return a,1,0
    d,x,y = exp_euc(b, a%b)
    d,x,y = d,y, x - (a//b)*y
    return d,x,y

def re(a,m):
    if m == 0: return a,1,0
    d,x,y = exp_euc(m, a%m)
    d,x,y = d,y, x - (a//m)*y
    return x


def simile(a,b,n):
    ress = []
    d = gcd(a,n) 
    n1 = n/d
    if gcd(a,n) == 1:
       x = (re(a,n)*b)%n
       return x

    else:
       if d > 1 and (b%d) != 0:
           print("no results")
       else:
           
           a1 = a/d
           b1 = b/d
           x = (b1*re(a1,n))%n1
           
           for i in range (d):
                x = x + i*n1
                x = int(x)
                ress.append(x)
       return ress
                
f = open('03.txt','r',encoding = 'utf8').read()
f = f.replace('\n','')

             
def decrypt(a,b,text):
    ress = []
    d = len(text)
    if d%2==0:
        for i in range (0, d//2 ,1):
            decrypted_text = (re(a,31**2)*(bi_ordo(text)[i] - b))%(31**2)
            x = bi_chro(decrypted_text)
            ress.append(x)
        return ress
    else:
        if d%2==1:
            for i in range (0,(d-1)//2,1):
                decrypted_text = (re(a,31**2)*(bi_ordo(text)[i] - b))%(31**2)
                x = bi_chro(decrypted_text)
                ress.append(x)
                
            return ress
       
d = decrypt(199,700,f)
f1 = ('mew.txt','w')

for item in d:
    f1.write("%s\n" % item)

#print(re(5,961))

most_rus_bi = 'стноентона'
most_common_bi = 'йаюачшрпюд'


for i in range(0,4):
    for j in range(0,5):
        for n in range(0,5):
            if n==j:
                continue
                x1 = bi_ordo(most_rus_bi)[j]
                x2 = bi_ordo(most_rus_bi)[n]
                y1 = bi_ordo(most_common_bi)[i]
                y2 = bi_ordo(most_common_bi)[i+1]
                a_l = simile((x1-x2),(y1-y2),961)
                for a in a_l:
                    k = (a,((y1-a*x1)%961))
                    keys.append(k)

for k in keys:
    print(str(k) + '\n')
    d = decrypt(k[0],k[1],f)
              if check(d) == 1:
                  print(d)






               
    


                    







import codecs
import re
from collections import Counter

alphabet='aбвгдeжзийклмнoпрстyфхцчшщьыэюя'

def OpenF(file):
 file_o=codecs.open(file,"r","utf-8")
 text=file_o.read()
 text=text.lower()
 default=re.compile('[^a-яa-Я]')
 text=default.sub('',text)
 return text;

def Index(text):
    chooseword=Counter(text)
    n=len(text)
    i=0
    for g in chooseword:
        i+=chooseword[g]*(chooseword[g]-1)
    i=i*(1/(n*(n-1)))
    return i

def Couple(text): 
    length=len(text)-1
    bigrams=[]
    for item in range(0,length,2):
        bigrams.append(text[item:item+2])    
    return bigrams


def makeXY(lst):
    x=0
    m=31
    MassiveStr=[]
    for i in range (len(lst)):
        x=lst[i][0]*m+lst[i][1]
        MassiveStr.append(x)
    return MassiveStr

def Lst(lst):
    List=[]
    for i in range(len(lst)):
        for g in alp:
            if lst[i][0]==g:
                a=alp[g]
            if lst[i][1]==g:
                b=alp[g]
        List.append(tuple((a,b)))
    return List

def ev(a,n):
    if n==0:
        return a,1,0
    else:
        d,x,y=ev(n,a%n)
        return d,y,x-y*(a//n)
def Check(tpl):
    a=0
    if tpl[1]<0:
        a=tpl[1]+31*31
    else:
        a=tpl[1]
    return (tpl[0],a,tpl[2])

def FindAB(X,Y):
    A=B=c=D=B1=A1=A11=N1=X0=0
    lstAB=[]
    lstX1=[]
    lstY1=[]
    lstA=[]
    m=31*31
    k=4
    z=4
    for i in range(4):
        for q in range(k):
            lstX1.append(((Check(ev(X[i]-X[i+1+q],m))),X[i],X[i+1+q]))

        k=k-1

    for i in range(4):
        for q in range(z):
            c=Y[i]-Y[i+1+q]
            #print(c)
            if c<0:
                c=m+c
            lstY1.append((c,Y[i]))
        z=z-1

    for i in range(len(lstX1)):
        if(lstX1[i][0]==1):
            for j in range(len(lstY1)):
                A=(lstX1[i][0][1]*lstY1[j][0])%(m)
                B=(lstY1[j][1]-lstX1[i][1])%(m)
                lstAB.append((A,B))
        else:
            for j in range(len(lstY1)):
                if (lstY1[j][0]%lstX1[i][0][0])==0:
                    D=lstX1[i][0][0]
                    if lstX1[i][1]-lstX1[i][2]<0:
                        c=lstX1[i][1]-lstX1[i][2]+m
                    else:
                        c=lstX1[i][1]-lstX1[i][2]
                    A1=(c)//D
                    B1=lstY1[j][0]//D
                    N1=m//D
                    A11=Check(ev(A1,N1))[1]
                    X0=(B1*A11)%N1
                    #print(X0)
                    for q in range(D):
                        A=X0+q*N1
                        B=(lstY1[j][1]-A*lstX1[i][1])%m
                        lstAB.append((A,B))            
    return(lstAB)

def D(A1,B,tlst):
    MassiveStr=[]
    for i in range(len(tlst)):
        MassiveStr.append((A1*(tlst[i]-B))%(31*31))
    return MassiveStr

def D1(lst):
    L=[]
    for i in range(len(lst)):
        a=lst[i]//31
        b=lst[i]%31
        L.append(a)
        L.append(b)  
    return L
def D2(lst):
    voides=''
    for i in range(len(lst)):
        for g in alp:
            if lst[i]==alp[g]:
                voides+=g
    return voides
def Decr(lst,text):
    bigrams=Couple(text)
    L=makeXY(Lst(bigrams))
    for i in range (len(lst)):
        A1=Check(ev(lst[i][0],31*31))[1]
        List=D(A1,lst[i][1],L)
        Ntext=D2(D1(List))
        if (Index(Ntext)>0.055):
            print("КЛЮЧ: (",lst[i][0],",",lst[i][1],")")
            print("I(X)= ",Index(Ntext))
            print()
            print("Текст который расшифровали")
            print(Ntext)
            break
       



lst1=['ст','нo','тo','нa','eн']
#open + mc
F=OpenF("03.txt")
bigrams=Couple(F)
a=Counter(bigrams)
b=a.most_common(5)
lst2=[]
for i in range(5):
    lst2.append(b[i][0])
print("Наиболее частые биграммы языка ",lst1)
print()
print("Наиболее частые биграммы шифртекста",lst2)
print()
print("Зашифрованный текст")
print(F)
print()

values=list()
for value in range(31):
    values.append(value)
alp={}
alp=dict(zip(alphabet,values))



L1=Lst(lst1)
L2=Lst(lst2)
X=makeXY(L1)
Y=makeXY(L2)
L=FindAB(X,Y)
Decr(L,F)
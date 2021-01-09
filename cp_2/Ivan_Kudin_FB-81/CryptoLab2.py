import string, re
from collections import Counter
 # шифрует, но удалить пунктуацию и вообще выделить очистку текста в отдельну ф-ю
with open("text.txt", 'rb') as file: Text = file.read().decode('UTF-8')
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
Letterintxt = Counter()
i = 0
j = 0
freq_sum = 0
text = Text.lower()
text = text.replace("ъ", "ь")
text = text.replace("ё", "е")
ctext = text.translate(str.maketrans('', '', string.punctuation))
cltext = ctext.translate(str.maketrans('', '', ' «»…–\n0123456789qwertyuiopasdfghjklzxcvbnm’\r\t„“— '))
print("Enter key:")
key = input()
file_name = 'ctext{}.txt'.format(len(key))
f = open(file_name, 'w')
while i < len(cltext):
             openLettnum = alphabet.index(cltext[i])                       # номер буквы текста в алфавите
             keyLettnum = (alphabet.index(key[i%len(key)]))             # номер буквы ключа в алфавите
             ciphLettnum = (openLettnum + keyLettnum) % len(alphabet)     # вычисляем номер шифрованой буквы
             f.write(alphabet[ciphLettnum])
             i = i+1
for i in cltext:
        Letterintxt[i] += 1      # подсчет частот
Letterintxt_sorted = list(Letterintxt.keys())
Letterintxt_sorted.sort()
for i in Letterintxt_sorted:
    print(i , ':', Letterintxt[i])
print(Letterintxt)      
for i in Letterintxt:
     freq_sum = freq_sum + Letterintxt[i]*(Letterintxt[i]-1)           
print(freq_sum)
conf_index = (1/(len(cltext)*(len(cltext)-1)))*freq_sum                   # индекс соответсвия       
print("Индекс соответсвия:", conf_index)
# дешифрование с известной длинной ключа
de_text = []
t = 0
while t < 17:
    de_text.insert(t, cltext[t:6517:17])
    t += 1 
print(de_text)
block_freq = Counter()
key_list = ''
for i in de_text:               # проходимся по блокам
    
             # считаем и достаем максимумы(даже если их несколько)
            for j in i:
                block_freq[j] += 1
            print(block_freq)
            block_freql = list(key for key, value in block_freq.items() 
                                   if value == max(block_freq.values()))
            print(block_freql)
            
            for l in block_freql:
               keyl1 = alphabet[(alphabet.index(l) - 14) % 32]
               keyl2 = alphabet[(alphabet.index(l) - 5) % 32]
               keyl3 = alphabet[(alphabet.index(l) - 0) % 32]
               keyl4 = alphabet[(alphabet.index(l) - 8) % 32]
               keyl5 = alphabet[(alphabet.index(l) - 13) % 32]
               key_list  = key_list + keyl1 + keyl2 + keyl3 + keyl4 +keyl5
            key_list = key_list + ','
            block_freq.clear()
            block_freql.clear()
print(key_list)
# расшифрование 
h = 0
openf = open('opened.txt', 'w')
key_list = 'войнамагаэндшпиль'
while h < len(cltext):
    ciphernum = alphabet.index(cltext[h])
    keynum = alphabet.index(key_list[h%len(key_list)])
    open = (ciphernum - keynum) % 32
    openf.write(alphabet[open])
    h = h + 1

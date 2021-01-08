# entropy counting in monograms and bigrams
# by Small_Wizard
import string, re
from itertools import islice
from math import log2
from collections import Counter
mono_entropy = 0
intersecting_entropy = 0
bigrams_entropy = 0
with open("text.txt", 'rb') as file: Text = file.read().decode('UTF-8')
text = Text.lower()
text = text.replace("ъ", "ь")
text = text.replace("ё", "е")
ctext = text.translate(str.maketrans('', '', string.punctuation))
cltext = ctext.translate(str.maketrans('', '', '«»…–\n0123456789qwertyuiopasdfghjklzxcvbnm’\r\t„“— '))
# считаем частоту для букв и сортируем
freq = Counter()
for i in cltext:
    freq[i] += 1 
freq_sorted = list(freq.keys())
freq_sorted.sort()
 # вывод
for i in freq_sorted:
    print(i, ':' ,freq[i]/len(cltext))
# ентропия для монограмм
for i in freq:
    mono_entropy = mono_entropy + (freq[i]/len(cltext))*(log2(freq[i]/len(cltext)))
print(mono_entropy*-1)
# отсортированная частота обычных биграмм 
bigrams = re.findall(r'..', cltext)     
bigrams_freq = Counter()
for i in bigrams:
    bigrams_freq[i] += 1
bigrams_freq_sorted = list(bigrams_freq.keys())
bigrams_freq_sorted.sort()
for i in bigrams_freq_sorted:
    print(i, ':',f'{ bigrams_freq[i]/len(cltext):.6f}')
# ентропия для биграмм
for i in bigrams_freq:
    bigrams_entropy = bigrams_entropy + (bigrams_freq[i]/len(cltext))*log2(bigrams_freq[i]/len(text))
print(bigrams_entropy*-1)
# отсортированая частота пересекающихся биграмм 
intersecting_bigrams = re.findall(r'.', cltext)
intersecting_bigrams =  Counter(zip(intersecting_bigrams, islice(intersecting_bigrams, 1, None)))
intersecting_bigrams_sorted = list(intersecting_bigrams.keys())
intersecting_bigrams_sorted.sort()
for i in intersecting_bigrams_sorted:
    print(i, ':', f'{intersecting_bigrams[i]/len(cltext):.6f}')
# ентропия для биграмм с пересечениями
for i in intersecting_bigrams:
    intersecting_entropy = intersecting_entropy + (intersecting_bigrams[i]/len(cltext))*log2(intersecting_bigrams[i]/len(text))
print((intersecting_entropy*-1)/2)


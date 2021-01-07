#!/bin/env python3
import numpy as np
import math
from collections import Counter

# with open('text123.txt', 'w') as f123:
#     f123.write(str2)

def actions( alph, fstr ):
	sum54 = 0
	a = {}
	fstr = fstr.lower()
	str2 = ''
	for i in fstr:
	    #   if i==len(fstr): break
		if i == ' ' and str2[-1] == ' ':
			continue
		if i in alph:
			str2 += i
		elif i == 'ё':
		        str2 += 'е'
		elif i == 'ъ':
			str2+='ь'
		
	print('----------------------------------------------------')
	c1 = 0
	for i in range(int((len(str2)/2))):
	    if str2[c1:c1 + 2] in a.keys():
	        a[str2[c1:c1 + 2]] += 1
	    else:
	        a[str2[c1:c1 + 2]] = 1
	    c1 += 2
	    
	sum4 = sum(a.values())
#	bigrams_b = []
#	for i in range(0,(len(str2)-2), 2):	
#		bigrams_b.append(str2[i:i+2])
#	bigrams_b1,cnt = np.unique(bigrams_b, return_counts=True)
#	p2 = cnt/np.sum(cnt)
#	H_b = -np.sum(p2 * np.log2(p2))/2
	res = Counter(str2[idx: idx + 2] for idx in range(len(str2) - 1))
	sum1 = sum(res.values())
	cnt = 0
	
	sum2 = 0
	
	for i in list(res.keys()):
	    sum2 = sum2 + (res[i]/sum1)*math.log2(res[i]/sum1)
	    res[i] = round((res[i]) / sum1, 3)
	
	sum3 = 0
	
	for i in list(a.keys()):
	    sum3 = sum3 + (a[i]/sum4)*math.log2(a[i]/sum4)
	    a[i] = round((a[i]) / sum4, 3)
	
	lst_nakl = list(res.items())
	
	lst_nakl.sort(key=lambda i: i[1], reverse=1)
	lst_wo_nakl = list(a.items())
	
	lst_wo_nakl.sort(key=lambda i: i[1], reverse=1)
	sum1 = 0
	for i in alph:
	    print('symbol "{0}" ---- {1}'.format(i, round((str2.count(i) / len(str2)), 3)))
	    sum54 = sum54 + ((str2.count(i) / len(str2)) * math.log2(str2.count(i) / len(str2)))
	
#	for i in range(len(lst_wo_nakl)):# lst_nakl, lst_wo_nakl:
#	    print('{0} {1}'.format(str(lst_nakl[i]),str(lst_wo_nakl[i])),i)
	print(lst_nakl)
	print(lst_wo_nakl)
	
	print('----------------------------------------------------')
	print('entropy simv- ' + str(sum54 * (-1)))
	print('entropy bigr z povt- ' + str(sum2/2 * (-1)))
	print('entropy bigr bez povt- ' + str(sum3/2 * (-1)))
	print('----------------------------------------------------')
	
	return


with open('text1', 'r') as f:
    fstr1 = f.read()

alph1 = "абвгдежзийклмнопрстуфхцчшщьюяыэ "
alph2 = "абвгдежзийклмнопрстуфхцчшщьюяыэ"
actions(alph1, fstr1)
actions(alph2, fstr1)

# for i in lst_nakl:
#     if cnt % 2 == 0:
#         print(i)
#     cnt += 1
#print(str2[:])

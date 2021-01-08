base = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
Nbase = "абвгдежзийклмнопрстуфхцчшщьыэюя"

from math import gcd as NOD
def modInverse(number, mod) : 				#функция "modInverse" - обратный элемент по модулю
    number %=  mod    								
    for current in range(1, mod,1) :
    	Flag = (number * current) % mod
    	if Flag != 1:
    		Flag = False
    	else:
    		return current

    return 1




def openCHAR(ch):							#функция "openCHAR" - зашифр. буква -> расшифр. буква
	first = base.find(ch)
	trueInD = (first - 14) % len(base)			#(текущая буква - "самая частая" по модулю (длина), где 14 - индекс буквы "о"(самая частая)
	return base[trueInD]						#возвращает реальное положение буквы
def openCHARforALLtxt(kCHAR,tCHAR):			#функция "openCHARforALLtxt" - зашифр. буква файла Виженера -> расшифр. буква файла
	tempINT = base.find(tCHAR) - base.find(kCHAR)
	return base[tempINT%len(base)]
def Converter(firstCHAR,secondCHAR):		#для расшифр. Афинного шифра
	tempARRAY = []
	tempARRAY = [Nbase.find(firstCHAR)*31,Nbase.find(secondCHAR)]
	
	return tempARRAY[0]+tempARRAY[1] 

def simile(a,b,c):                         #для  сравнений
	result = list()
	nod_ac = NOD(a,c)

	if nod_ac == 1:
		flag = False
	else:
		flag = True
	if b % nod_ac != 0:
		Flag = False
	else:
		Flag = True
	if(flag):
		if(Flag):
			temp = {}  								#словарь
			temp['a']= a/nod_ac
			temp['b']= b/nod_ac
			temp['c']= c/nod_ac
			for index in range(0,nod_ac,1):
				tempINT = modInverse(temp['a'],temp['c'])
				tempINT += index*temp['c']
				tempINT %= temp['c']
				result.append(tempINT)
	else:
		temp = (modInverse(a,c)*b)
		temp%=c
		result.append(temp)
	return result





	
with open('01.txt') as dataFile:
	data = dataFile.read()				

data = [data[i:i+2] for i in range(0, len(data), 2)] #делим строку по 2 символа
#print(data)
Temp_arr,LenArr = [],len(data)						#записываем биграммы в массив
for i in base:
	for j in base:
		TempINT = data.count((i+j)) 
		Temp_arr.append(TempINT)
		

Temp_arr.sort()
Temp_arr = Temp_arr[len(Temp_arr)-5:len(Temp_arr)]
#print(Temp_arr)
tempARR,temp = [],[]

for i in base:
	for j in base:
		if data.count((i+j)) in Temp_arr:
			tempARR.append(i+j)
for index in tempARR:

	temp.append(Converter(index[0],index[1]))
		


print("most common bigrams:",tempARR,temp)              

pareARR,baseFreq = [],['ст', 'но', 'то', 'на', 'ен']    #5 найденных биграмм и 5 статических, сопоставляем и решаем уравнение
arr = []
for index1 in baseFreq:
	for index2 in tempARR:
		for index3 in baseFreq:
			for index4 in tempARR:
				IndexARR = [index1,index2,index3,index4]
				IndexARR = list(set(IndexARR))
				if (len(IndexARR)) == 4:
					dataDICT = {}
					divX=Converter(index1[0],index1[1])-Converter(index3[0],index3[1])
					divY=Converter(index2[0],index2[1])-Converter(index4[0],index4[1])
					dataDICT['x']=Converter(index1[0],index1[1])
					dataDICT['y']=Converter(index2[0],index2[1])
					dataDICT['M'] = 31*31
					arrAy = simile((divX),(divY),dataDICT['M'])
					for ind in arrAy:
						second = (dataDICT['y']-ind*dataDICT['x'])
						second%=dataDICT['M']
						arr+=[[ind,second]]
	
	
flag = True					
for i in range(0,len(arr),1):
	tempSTR = str()
	for j in range(0,len(data),1):
		dataDICT = dict()
		dataDICT['y'] = Converter(data[j][0],data[j][1])
		dataDICT['temp'] = modInverse(arr[i][0],961)*(dataDICT['y']-arr[i][1])%961
		dataDICT['s'] = dataDICT['temp']%31
		dataDICT['f'] = (dataDICT['temp'] - dataDICT['s'])//31

		tempSTR += Nbase[dataDICT['f']]+ Nbase[dataDICT['s']]
	tempIND = 0
	for jedex in Nbase:
		tempINT = tempSTR.count(jedex,0,len(tempSTR))
		tempIND += ((tempINT -1)/(len(tempSTR)-1))*(tempINT/len(tempSTR)) #ищем индекс соответствтия
		
	if tempIND > 0.05:     #сопоставление индекса соответствия
		f= open('#{}#.txt'.format(arr[i]), 'w')
		f.write(tempSTR)
		f.close()
		flag = False       #если flag = False - выходим из цикла при этом сохраняем разшифр. текст в файл в котором ключи есть

	if flag == False:
		i += 1000


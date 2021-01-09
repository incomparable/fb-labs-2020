import string
from array import *
# Обрахування частоти появи символів у блоці N(Y) та індексу відповідності
def IndexCounter(BlockText):
    j=0
    Y = array('I',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ) # значення частот символів російського алфавіту (32 символи)
    for i in 'абвгдежзийклмнопрстуфхцчшщъыьэюя': # для усіх символів алфавіту визначаємо кількість входжень у блок
        Y[j]=BlockText.count(i)
        j+=1
    IS=0
    j=0
    # В масиві - кількість входжень символів в блоку Y - Nt(Y)
    # Далі - рахуємо суму по всім символам алфавіту
    for k in 'абвгдежзийклмнопрстуфхцчшщъыьэюя':
        I=Y[j]*(Y[j]-1)
        IS+=I
        j+=1
    return IS
# Обрахування індексів відповідності довжини ключа шифра Віжінеру 1-м методом (порівняння індексів відповідності для відкритого та шифртекстів
def KeyLenthVizinerISFM(ChipherText,KeyLen):
    LText=len(ChipherText)
    for i in range(LText-KeyLen):
        BlockCText=ChipherText[i:i+KeyLen]
        I=IndexCounter(BlockCText)
        I=I/(KeyLen*(KeyLen-1))
    return I
# Індекс відповідності для відкритого тексту (російська мова) приблизно дорівнює 0,055
# порівнюємо із середнім для блоків різної довжини

def main():
   #Открытие файла + заготовки для форматирования исходного текста
   with open("cipher.txt", 'rb') as file:  CipherTextControl = file.read().decode('utf-8')
   for i in range(2,20):
        I2=KeyLenthVizinerISFM(CipherTextControl,i)
        print(i,I2)
   return 0

main()


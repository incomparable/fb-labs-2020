from collections import Counter
import re

class Decrypt:
	def __init__(self):
		self.file_in = ''
		self.encoding = ''
		self.key_block = []
		self.key = ''
		self.decrypt = ''

		self.alpha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
		self.length_alpha = len(self.alpha)
		self.length_key = []
		self.alpha_freq = { 
			'а': 0.075, 'б': 0.017, 'в': 0.046, 'г': 0.016, 'д': 0.03, 'е': 0.088, 'ж': 0.008, 'з': 0.019, 'и': 0.075, 'й': 0.012, 'к': 0.034, 'л': 0.042, 'м': 0.032, 'н': 0.064, 'о': 0.109, 'п': 0.028, 'р': 0.048, 'с': 0.054, 'т': 0.064, 'у': 0.026, 'ф': 0.002, 'х': 0.011, 'ц': 0.005, 'ч': 0.015, 'ш': 0.007, 'щ': 0.004, 'ъ': 0.017, 'ы': 0.019, 'ь': 0.017, 'э': 0.004, 'ю': 0.007, 'я': 0.022
		}
		self.main()
		
	def main(self):
		print("\nВведите файл для расшифровки: ")
		self.file_in = str(input())
			
		print("\nВведите кодировку файла: ")
		self.encoding = str(input())

		print('\nИндексы длины ключей:')
		for i in range(2, 31):
			self.break_key_block(i)

		if not self.length_key:
			print('\nОшибка! Не удалось найти длину ключа!')
			return

		print("\nВозможная длина ключа: {}".format(self.length_key))
		print("\nВведите длину ключа: ")
		self.break_key_block(int(input()))
			
		self.get_key()
		print('\nВаш ключ: {}'.format(self.key))
					
		self.decrypt_text()
		self.write_results()

	def break_key_block(self, step_block):
		self.key_block = []
		sum_index = 0

		for i in range(step_block):
			alpha_block = {}
			step_current = i + 1
			count = 0

			with open(self.file_in, encoding=self.encoding) as f:
				for line in f:
					for j in range(len(line)):
						if step_current != step_block:
							step_current += 1
						else:
							step_current = 1
							count += 1

							try:
								alpha_block[line[j]] += 1
							except:
								alpha_block[line[j]] = 1

				index = 0
				for e in alpha_block:
					index += (alpha_block[e] * (alpha_block[e] - 1.0))

				sum_index = ((1.0 / (count * (count - 1.0))) * index) + sum_index
				self.key_block.append(alpha_block)

		self.check_index(sum_index, step_block)
		
	def check_index(self, index, step):
		print('{}: {}'.format(step, index / step))
		if index / step > 0.0553 and not step in self.length_key:
			self.length_key.append(step)

	def get_key(self):
		for s in reversed(self.key_block):
			my_max = 0

			for i in range(self.length_alpha):
				my_sum = 0

				for e in self.alpha_freq:
					try:
						my_sum += self.alpha_freq[e] * s[self.alpha[(self.alpha.index(e) + i) % self.length_alpha]]
					except:
						break

				if my_sum > my_max:
					my_max = my_sum
					a = 'п' if self.alpha[i] == 'ч' else self.alpha[i]

			try:
				self.key += a
			except:
				break

	def decrypt_text(self):
		text = open(self.file_in, encoding=self.encoding).read()

		step = 0
		length = len(self.key)
		for a in text:
			if a in self.alpha:
				self.decrypt += str(self.alpha[(ord(a) - ord(self.key[step]) + self.length_alpha) % self.length_alpha])
				step = 0 if step == (length - 1) else step + 1
			else:
				self.decrypt += a

	def write_results(self):
		file_out = "decrypt_{}".format(self.file_in)
		fopen = open(file_out, 'w', encoding='utf-8')
		fopen.write("Ваш ключ: {}\n\n".format(self.key))
		fopen.write(self.decrypt)
		fopen.close()
		print('Расшифрованный текст в: {}'.format(file_out))

class Encrypt:
	def __init__(self):
		self.file_in = ''
		self.encoding = ''
		self.length_key = 0
		self.key = ''
		self.encrypt = ''
		self.text = ''
		self.length_text = 0
		self.index = 0
		
		self.alpha = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
		self.length_alpha = len(self.alpha)

		self.keys = {
			2 : 'он',
			3 : 'кот',
			4 : 'икра',
			5 : 'грона',
			10 : 'элегантный',
			11 : 'ясновидящий',
			12 : 'кинематограф',
			13 : 'месторождение',
			14 : 'противогазовый',
			15 : 'соотечественник',
			16 : 'прочувствованный',
			17 : 'нетрудноспособный',
			18 : 'высокопоставленный',
			19 : 'товаропроизводитель',
			20 : 'золотопромышленность'
			
		}
		
		self.main()
		
	def main(self):
		print("\nВведите файл для шифровки: ")
		self.file_in = str(input())
			
		print("\nВведите кодировку файла: ")
		self.encoding = str(input())

		print("\nВведите длину ключа: ")
		self.length_key = int(input())
		
		if not self.length_key in self.keys:
			print('\nОшибка! Длина ключа должна быть 2-5 или 10-20!')
			return

		self.key = self.keys[self.length_key]
		
		self.clear_text()
		self.check_index(self.text)
		print("\nИндекс открытого текста: {}".format(self.index))
		
		self.encrypt_text()
		self.check_index(self.encrypt)
		print("Индекс зашифрованого текста: {}".format(self.index))
				
		self.write_results()

	def check_index(self, text):
		self.index = 0
		count = Counter(text)
		for a in count:
			self.index += count[a] * (count[a] - 1.0)

		self.index /= self.length_text * (self.length_text - 1.0)
		
	
	def clear_text(self):
		self.text = ' '.join((open(self.file_in, encoding=self.encoding).read()).split())
		cleared_text = ''

		for symbol in self.text:
			find = re.match('[а-я]$', symbol.lower())
			if find:
				symbol = find.group(0)
				if symbol == 'ъ':
					symbol = 'ь'
				elif symbol == 'ё':
					symbol = 'е'

				cleared_text += str(symbol)
		
		self.text = ' '.join(cleared_text.split())
		self.length_text = len(self.text)
	
	def encrypt_text(self):
		step = 0
		for a in self.text:
			if a in self.alpha:
				self.encrypt += str(self.alpha[(self.alpha.index(a) + self.alpha.index(self.key[step])) % self.length_alpha])
				step = (step + 1) if step != (self.length_key - 1) else 0

	def write_results(self):
		file_out = "encrypt_{}_{}".format(self.length_key, self.file_in)
		fopen = open(file_out, 'w', encoding='utf-8')
		fopen.write("Ключ шифровки: {}\n\n".format(self.key))
		fopen.write(self.encrypt)
		fopen.close()
		print('\nЗашифрованный текст в: {}'.format(file_out))

		
if __name__ == '__main__':
	print("Режим: Шифровка / Расшифровка = 0 / 1")
	if int(input()) == 1:
		Decrypt()
	else:
		Encrypt()

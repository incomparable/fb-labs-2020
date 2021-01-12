import re

def main():
	print("\nВведите файл для чтения: ")
	file = str(input())

	print("\nВведите длину ключа от 2 до 20: ")
	length = int(input())

	text = open(file, encoding = 'utf-8').read()

	dict = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
	keys = {
		2    : "ат",
		3    : "ыко",
		4    : "гдат",
		5    : "оспор",
		10   : "илстишиной",
		11   : "какжальчто",
		12   : "ничеготынеу",
		13   : "слышаллишьтро",
		14   : "ньеебеззвучную",
		15   : "струнуитыпоймеш",
		16   : "ьчтоможнодажетиш",
		17   : "шеатынечувствовал",
		18   : "какпахнеттишинойве",
		19   : "дьзапахунеенастольк",
		20   : "онежныйявароматеэтом"
	}

	key = keys[length]
	step = 0
	encrypt = ''

	for symbol in text:
		symbol = symbol.lower()

		if symbol in dict:
			encrypt += dict[(dict.index(symbol) + dict.index(key[step])) % len(dict)]

			if step == len(key) - 1:
				step = 0
			else:
				step += 1

	file = 'out_{}_{}'.format(length, file)
	print('\nТекс зашиврован и выведен в файл: {}'.format(file))

	file = open(file, 'w', encoding = 'utf-8')
	file.write(encrypt)
	file.close()

if __name__ == '__main__':
	main()

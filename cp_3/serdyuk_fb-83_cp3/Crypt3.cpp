#include "pch.h"
#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>
#include <fstream>

using namespace std;

ifstream ifs;
ofstream ofs;
string alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя";
string str;
string Ostr;
bool notAccept = 0;
int accepted = 0;
int Xi;
int Yi;
double Xidm;
double Xirm;
const int modul = 31;
const int num = 5;
int OTbigrams1[2*num]; //для запису номерів літер найчастіших біграм ВТ
int OTbigrams2[num];
int CTbigrams1[2*num]; //для запису номерів літер найчастіших біграм ШТ
int CTbigrams2[num];
double no_cross_bigram_frequency[modul][modul];
int a = 1;
int b = 0;
int a_1;

void CT_freq_bigrams(string s, int num)
{
	double count;
	//cout << s.length();

	for (int i = 0; i < 2 * num; i++)
	{
		CTbigrams1[i] = 0;
	}

	for (int i = 0; i < num; i++)
	{
		CTbigrams2[i] = 0;
	}

	for (int i = 0; i < modul; i++)
	{
		count = 0;

		for (int j = 0; j < modul; j++)
		{
			count = 0;

			for (int k = 0; k < s.length() - 1; k += 2)
			{
				if (s[k] == alphabet[i] && s[k + 1] == alphabet[j])
				{
					count++;
					//cout << s[k] << " " << s[k + 1] << "\n";
				}
			}
			
			if ((int)s.length() % 2 == 0) no_cross_bigram_frequency[i][j] = 2 * count / s.length();
			if ((int)s.length() % 2 == 1) no_cross_bigram_frequency[i][j] = 2 * count / (s.length() - 1);

			ofs << "\t" << setprecision(6) << no_cross_bigram_frequency[i][j];

			count = 0;

			for (int l = 0; l < 2 * num; l += 2)
			{
				if (no_cross_bigram_frequency[i][j] > no_cross_bigram_frequency[CTbigrams1[l]][CTbigrams1[l + 1]])
					count++;
			}

			for (int l = 0; l < 2 * num; l += 2)
			{
				if (count > l / 2)
				{
					if (l >= 2)
					{
						CTbigrams1[2 * num - l] = CTbigrams1[2 * num - 2 - l];
						CTbigrams1[2 * num + 1 - l] = CTbigrams1[2 * num - 1 - l];
					}

					CTbigrams1[2 * num - 2 - l] = i;
					CTbigrams1[2 * num - 1 - l] = j;
				}
			}

		}
		ofs << "\n";

		for (int l = 0; l < 2 * num; l++)
		{
			ofs << "\t" << CTbigrams1[l];
		}
		ofs << "\n";

		for (int l = 0; l < num; l++)
		{
			CTbigrams2[l] = modul * CTbigrams1[2 * l] + CTbigrams1[2 * l + 1];
			ofs << "\t\t" << CTbigrams2[l];
		}
	}
}

int evklid(int a, int n)
{
	int r[modul];
	int q[modul];
	int v[modul];

	r[0] = n;
	r[1] = a;
	q[0] = 1;
	v[0] = 0;
	v[1] = 1;

	cout << "\n\n" << n << " " << a;
	int i = 1;

	while (r[i - 1] % r[i] != 0)
	{
		q[i] = r[i - 1] / r[i];
		r[i + 1] = r[i - 1] % r[i];
		v[i + 1] = v[i - 1] - v[i] * q[i];
		cout << "\n" << r[i] << " " << q[i] << " " << r[i + 1] << " " << v[i + 1];
		i++;
	}

	cout << "\n" << (v[i] + n) % n;
	return (v[i] + n) % n;
}

string decipher(string s, int CTb1, int CTb2, int OTb1, int OTb2, int p)
{
	Ostr = "";
	a = (((modul * modul + CTbigrams2[CTb1] - CTbigrams2[CTb2]) % (modul * modul)) * evklid((modul * modul + OTbigrams2[OTb1] - OTbigrams2[OTb2]) % (modul * modul), modul * modul)) % (modul * modul);
	b = ((int)pow(modul, 4) + CTbigrams2[CTb1] - OTbigrams2[OTb1] * a) % (modul * modul);

	cout << "\n\n" << p << "\n(" << a << ", " << b << ")";
	a_1 = evklid(a, modul * modul);
	cout << "\n\n\n";

	for (int k = 0; k < s.length() - 1; k += 2)
	{
		for (int i = 0; i < modul; i++)
		{
			if (s[k] == alphabet[i])
				Xidm = i;
			if (s[k + 1] == alphabet[i])
				Xirm = i;
		}
		Yi = (int)(Xidm * modul + Xirm);
		Xi = ((int)pow(modul, 4) + a_1 * (Yi - b)) % (modul * modul);

		Xidm = Xi / modul;
		Xirm = Xi % modul;

		//cout << "\n\n" << Yi << " " << Xidm << " " << Xirm;

		Ostr += alphabet[(int)Xidm];
		Ostr += alphabet[Xirm];
	}

	return Ostr;
}

void check(string s)
{
	ofs << "\n\n";
	cout << "\n" << s.length() << "\n";
	double Count = 0.000000;
	notAccept = 0;

	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == 0 && s[k + 1] == 27)
			Count++;
	}

	cout << "аь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[5] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "еь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[8] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "иь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[9] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "йь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[19] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "уь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[26] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "ыь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[27] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "ьь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[28] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "эь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[29] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "юь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[30] && s[k + 1] == alphabet[27])
			Count++;
	}

	cout << "яь: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[27] && s[k + 1] == alphabet[26])
			Count++;
	}

	cout << "ьы: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() > 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[17] && s[k + 1] == alphabet[18])
			Count++;
	}

	cout << "ст: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() < 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[13] && s[k + 1] == alphabet[14])
			Count++;
	}

	cout << "но: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() < 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[18] && s[k + 1] == alphabet[14])
			Count++;
	}

	cout << "то: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() < 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[13] && s[k + 1] == alphabet[0])
			Count++;
	}

	cout << "на: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() < 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	Count = 0;
	for (int k = 0; k < s.length() - 1; k++)
	{
		if (s[k] == alphabet[5] && s[k + 1] == alphabet[13])
			Count++;
	}

	cout << "ен: ";
	cout << 2 * Count / s.length() << "\n";
	if (2 * Count / s.length() < 0.002 && notAccept == 0)
	{
		ofs << "This text is not acceptable.\n";
		cout << "This text is not acceptable.\n";
		notAccept = 1;
	}

	if (notAccept == 0)
	{
		ofs << "THIS text is probably acceptable.\n";
		cout << "THIS text is probably acceptable.\n";
		accepted++;
	}
}

int main()
{
	setlocale(LC_ALL, "rus");

	char c[30000];

	ifs.open("19.txt");
	ofs.open("out.txt");

	while (!ifs.eof())
	{
		ifs.getline(c, 300);
		str += c;
	}

	//ofs << str;
	CT_freq_bigrams(str, 5);

	OTbigrams1[0] = 17;
	OTbigrams1[1] = 18;
	OTbigrams1[2] = 13;
	OTbigrams1[3] = 14;
	OTbigrams1[4] = 18;
	OTbigrams1[5] = 14;
	OTbigrams1[6] = 13;
	OTbigrams1[7] = 0;
	OTbigrams1[8] = 5;
	OTbigrams1[9] = 13;

	for (int l = 0; l < num; l++)
	{
		OTbigrams2[l] = modul * OTbigrams1[2 * l] + OTbigrams1[2 * l + 1];
		cout << " " << OTbigrams2[l];
	}

	//evklid(17, 129);

	int p = 0;
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 1, 0, 1, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 0, 0, 1, p);
	check(Ostr);

	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 1, 0, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 1, 1, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 0, 0, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 0, 1, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 2, 0, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 2, 1, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 0, 0, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 0, 1, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 2, 0, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 2, 1, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 1, 0, 2, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 1, 1, 2, p);
	check(Ostr);

	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 1, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 1, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 1, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 0, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 0, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 0, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 2, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 2, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 2, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 0, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 0, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 0, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 2, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 2, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 2, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 1, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 1, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 1, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 3, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 3, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 0, 3, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 0, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 0, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 0, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 2, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 2, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 2, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 3, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 3, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 2, 3, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 3, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 3, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 1, 3, 2, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 1, 0, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 1, 1, 3, p);
	check(Ostr);
	ofs << "\n\n\n" << ++p << "\n" << decipher(str, 3, 1, 2, 3, p);
	check(Ostr);

	ofs << "\n\n" << accepted << " accepted texts";
	cout << "\n\n" << accepted << " accepted texts";

	ifs.close();
	ofs.close();
}
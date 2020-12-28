#include "pch.h"
#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>
#include <fstream>
using namespace std;

int main()
{
	setlocale(LC_ALL, "rus");

	ifstream f;
	ofstream ofs;
	
	char c[5000];
	string s;
	double count = 0.000000;
	double sz;
	char ans;
	int modul = 32;

	cout << "Your text with spaces?" << endl;
	cin >> ans;

	if (ans == 'n')
	{
		modul = 31;
		f.open("text1.txt");

		while (!f.eof())
		{
			f.getline(c, 5000);
			s += c;
		}

		sz = s.length();
		cout << "Your modulus is " << modul << "\n";
	}
	else
	{
		modul = 32;
		f.open("text2.txt");

		while (!f.eof())
		{
			f.getline(c, 5000);
			s += c;
			s += " ";
		}

		sz = s.length();
		s.resize(sz - 1);
		sz = s.length();
		cout << "Your modulus is " << modul << "\n";
	}

	f.close();
	ofs.open("output.txt");

	//char alphabet[32] = { "а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я", " " };
	string alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя ";
	double frequency[32];
	double enthropy = 0;
	double nadlyshkovist = 0;

	double cross_bigram_frequency[32][32];
	double cross_bigram_enthropy = 0.000000;
	double cross_bigram_nadlyshkovist = 0.000000;
	double no_cross_bigram_frequency[32][32];
	double no_cross_bigram_enthropy = 0.000000;
	double no_cross_bigram_nadlyshkovist = 0.000000;


	for (int i = 0; i < modul; i++)
	{
		count = 0;

		for (int j = 0; j < sz; j++)
		{
			if (s[j] == alphabet[i])
			{
				count++;
			}
		}
		frequency[i] = count / sz;
		ofs << alphabet[i] << "\t" << setprecision(6) << frequency[i] << "\n";
		enthropy += frequency[i] * log2(frequency[i]);
	}
	enthropy = -enthropy;
	nadlyshkovist = 1 - (enthropy / log2(modul));
	ofs << "\n\n" << enthropy << "\n" << nadlyshkovist << "\n\n";


	for (int i = 0; i < modul; i++)
	{
		count = 0;

		for (int j = 0; j < modul; j++)
		{
			count = 0;

			for (int k = 0; k < sz - 1; k++)
			{
				if (s[k] == alphabet[i] && s[k+1] == alphabet[j])
				{
					count++;
				}
			}
			cross_bigram_frequency[i][j] = count / (sz - 1);

			ofs << "\t" << setprecision(6) << cross_bigram_frequency[i][j];

			if (cross_bigram_frequency[i][j] == 0) cross_bigram_frequency[i][j] = 0.00000001;

			cross_bigram_enthropy += cross_bigram_frequency[i][j] * log2(cross_bigram_frequency[i][j]);
		}
		ofs << "\n";
	}

	cross_bigram_enthropy = -0.5 * cross_bigram_enthropy;
	cross_bigram_nadlyshkovist = 1 - (cross_bigram_enthropy / log2(modul));
	ofs << "\n\n" << cross_bigram_enthropy << "\n" << cross_bigram_nadlyshkovist << "\n\n";


	for (int i = 0; i < modul; i++)
	{
		count = 0;

		for (int j = 0; j < modul; j++)
		{
			count = 0;

			for (int k = 0; k < sz - 1; k+=2)
			{
				if (s[k] == alphabet[i] && s[k + 1] == alphabet[j])
				{
					count++;
				}
			}

			if ((int)sz % 2 == 0) no_cross_bigram_frequency[i][j] = 2 * count / sz;
			if ((int)sz % 2 == 1) no_cross_bigram_frequency[i][j] = 2 * count / (sz - 1);

			ofs << "\t" << setprecision(6) << no_cross_bigram_frequency[i][j];

			if (no_cross_bigram_frequency[i][j] == 0) no_cross_bigram_frequency[i][j] = 0.00000001;

			no_cross_bigram_enthropy += no_cross_bigram_frequency[i][j] * log2(no_cross_bigram_frequency[i][j]);
		}
		ofs << "\n";
	}

	no_cross_bigram_enthropy = -0.5 * no_cross_bigram_enthropy;
	no_cross_bigram_nadlyshkovist = 1 - (no_cross_bigram_enthropy / log2(modul));
	ofs << "\n\n" << no_cross_bigram_enthropy << "\n" << no_cross_bigram_nadlyshkovist << "\n\n";

	ofs.close();
}
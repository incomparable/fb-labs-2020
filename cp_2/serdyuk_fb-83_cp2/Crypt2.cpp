#include "pch.h"
#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>
#include <fstream>
#include <Windows.h>
using namespace std;

int oper1 = 0, oper2 = 0;
string sum(5000, 'а');
string temp_sum;
int period;
int ki;
int sum_index = 0;
int Count = 0;
double fi;
string alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя";

string encipher(string s, string k)
{
	period = k.length();

	for (int i = 0; i < s.length(); i++)
	{
		ki = i % period;
		for (int j = 0; j < 32; j++)
		{
			if (s[i] == alphabet[j])
				oper1 = j;
			if (k[ki] == alphabet[j])
				oper2 = j;
		}

		sum_index = (oper1 + oper2) % 32;
		sum[i] = alphabet[sum_index];
	}
	return sum.substr(0, s.length());
}

double indexCount(string s)
{
	fi = 0.000000;

	for (int i = 0; i < 32; i++)
	{
		Count = 0;

		for (int j = 0; j < s.length(); j++)
		{
			if (s[j] == alphabet[i])
			{
				Count++;
			}
		}
		fi += Count * (Count - 1);
	}
	//cout << fi << " " << s.length() << " " << (s.length() * (s.length() - 1)) << endl;
	return fi / (s.length() * (s.length() - 1));
}

int sameCount(string s, int per)
{
	Count = 0;

	for (int i = 0; i < s.length() - per; i++)
	{
		if (s[i] == s[i + per]) //символ Крокенера
			Count++;
	}

	return Count;
}

string findKey(string s, int per, int ch)
{
	int maxCount;
	int maxI;
	int currI;
	temp_sum = "";

	for (int h = 0; h < per; h++)
	{
		maxCount = 0;
		maxI = 0;

		for (int i = 0; i < 32; i++)
		{
			Count = 0;

			for (int j = h; j < s.length(); j+=per)
			{
				if (s[j] == alphabet[i])
				{
					Count++;
				}
			}
			if (Count > maxCount)
			{
				maxCount = Count;
				maxI = i;
			}
		}
		currI = (32 + maxI - ch) % 32;
		temp_sum += alphabet[currI];
	}
	return temp_sum;
}

string decipher(string s, string k)
{
	period = k.length();

	for (int i = 0; i < s.length(); i++)
	{
		ki = i % period;
		for (int j = 0; j < 32; j++)
		{
			if (s[i] == alphabet[j])
				oper1 = j;
			if (k[ki] == alphabet[j])
				oper2 = j;
		}

		sum_index = abs(32 + oper1 - oper2) % 32;
		sum[i] = alphabet[sum_index];
	}
	return sum.substr(0, s.length());
}

int main()
{
	setlocale(LC_ALL, "rus");
	//SetConsoleCP(1251);
	//SetConsoleOutputCP(1251);

	ifstream ifs;
	ofstream ofs, ofs2, ofs3, ofs4, ofs5, ofs15;
	char c[25000];
	string key1, key2, key3, key4, key5;
	string inp1, inp2;

	ifs.open("keys.txt");

	ifs.getline(c, 50);
	key1 = c;
	ifs.getline(c, 50);
	key2 = c;
	ifs.getline(c, 50);
	key3 = c;
	ifs.getline(c, 50);
	key4 = c;
	ifs.getline(c, 50);
	key5 = c;

	ifs.close();
	ifs.open("input1.txt");
	ofs2.open("out2r.txt");
	ofs3.open("out3r.txt");
	ofs4.open("out4r.txt");
	ofs5.open("out5r.txt");
	ofs15.open("out15r.txt");

	ifs.getline(c, 5000);
	inp1 = c;

	cout << indexCount(inp1) << endl;

	temp_sum = encipher(inp1, key1);
	ofs2 << temp_sum << "\n";
	ofs2 << indexCount(temp_sum) << "\n";

	temp_sum = encipher(inp1, key2);
	ofs3 << temp_sum << "\n";
	ofs3 << indexCount(temp_sum) << "\n";

	temp_sum = encipher(inp1, key3);
	ofs4 << temp_sum << "\n";
	ofs4 << indexCount(temp_sum) << "\n";

	temp_sum = encipher(inp1, key4);
	ofs5 << temp_sum << "\n";
	ofs5 << indexCount(temp_sum) << "\n";

	temp_sum = encipher(inp1, key5);
	ofs15 << temp_sum << "\n";
	ofs15 << indexCount(temp_sum) << "\n";

	ofs2.close();
	ofs3.close();
	ofs4.close();
	ofs5.close();
	ofs15.close();
	ifs.close();
	ifs.open("input2.txt");
	ofs.open("output2.txt");

	ifs.getline(c, 5000);
	inp2 = c;

	ofs << indexCount(inp2) << endl << endl;

	ofs << "1\t" << sameCount(inp2, 1) << endl;
	ofs << "2\t" << sameCount(inp2, 2) << endl;
	ofs << "3\t" << sameCount(inp2, 3) << endl;
	ofs << "4\t" << sameCount(inp2, 4) << endl;
	ofs << "5\t" << sameCount(inp2, 5) << endl;
	ofs << "6\t" << sameCount(inp2, 6) << endl;
	ofs << "7\t" << sameCount(inp2, 7) << endl;
	ofs << "8\t" << sameCount(inp2, 8) << endl;
	ofs << "9\t" << sameCount(inp2, 9) << endl;
	ofs << "10\t" << sameCount(inp2, 10) << endl;
	ofs << "11\t" << sameCount(inp2, 11) << endl;
	ofs << "12\t" << sameCount(inp2, 12) << endl;
	ofs << "13\t" << sameCount(inp2, 13) << endl;
	ofs << "14\t" << sameCount(inp2, 14) << endl;
	ofs << "15\t" << sameCount(inp2, 15) << endl;
	ofs << "16\t" << sameCount(inp2, 16) << endl;
	ofs << "17\t" << sameCount(inp2, 17) << endl;
	ofs << "18\t" << sameCount(inp2, 18) << endl;
	ofs << "19\t" << sameCount(inp2, 19) << endl;
	ofs << "20\t" << sameCount(inp2, 20) << endl;
	ofs << "21\t" << sameCount(inp2, 21) << endl;
	ofs << "22\t" << sameCount(inp2, 22) << endl;
	ofs << "23\t" << sameCount(inp2, 23) << endl;
	ofs << "24\t" << sameCount(inp2, 24) << endl;
	ofs << "25\t" << sameCount(inp2, 25) << endl;
	ofs << "26\t" << sameCount(inp2, 26) << endl;
	ofs << "27\t" << sameCount(inp2, 27) << endl;
	ofs << "28\t" << sameCount(inp2, 28) << endl;
	ofs << "29\t" << sameCount(inp2, 29) << endl;
	ofs << "30\t" << sameCount(inp2, 30) << endl;
	ofs << "31\t" << sameCount(inp2, 31) << endl;
	ofs << "32\t" << sameCount(inp2, 32) << endl;
	ofs << "33\t" << sameCount(inp2, 33) << endl;

	ofs << findKey(inp2, 16, 14) << "\n";
	ofs << findKey(inp2, 16, 5) << "\n";
	ofs << findKey(inp2, 16, 0) << "\n";
	ofs << findKey(inp2, 16, 8) << "\n";
	ofs << findKey(inp2, 16, 13) << "\n";
	
	temp_sum = decipher(inp2, "братьякарамазовы");
	ofs << "\n" << temp_sum << "\n";

	ofs.close();
}
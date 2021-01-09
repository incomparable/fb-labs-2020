#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#define calcfs(x, y) 		((31 * x + y))
#define calc_a 				(calculate_a(data, data->russian[i] - data->russian[j], data->best_cand[l] - data->best_cand[k], 4))
#define calc_b 				(calculate_b(data, 0, data->russian[i], data->best_cand[l]))

#define calc_more_b 		(q = a / b, r = a - q * b, *x = x2 - q * x1, a = b, b = r, x2 = x1, x1 = *x, y2 = y1, y1 = *y)


int calc(int a, int b, int *x, int *y)
{
	int q, r, x1, x2, y1, y2;
	x2 = 1; x1 = 0; y2 = 0; y1 = 1;
	
	if (b == 0)
	{
		(*x = 1, *y = 0);
		return (a);
	}
	
	while (b > 0)
		calc_more_b;

	*x = x2;
	*y = y2;
	return (a);
}

int evklid(int a, int n)
{
	int d, x, y;
	if (calc(a, n, &x, &y) != 1)
		return (0);
		
	while (x > 0)
		return x;
		   
	return (n + x);
}

struct all_data
{
	wchar_t *alp;
	char	*filename;
	int	file_size;
	int	bigram_size;
	int	*bigram_text;
	int	*count_bigrams;
	int	size_alpha;
	int	best_cand[5];
	int	russian[5];
	int	*a = NULL;
	int	*b = NULL;
	int	size_mas;
	wstring str;
	wfstream file;
};

int find_alpha(all_data *data, wchar_t c)
{
	int i = -1;
    for (; ++i < 31;)
            if(data->alp[i] == c)
                    return (i);
                    
    return (-1);
}

void russian(all_data *data, wchar_t *first, wchar_t *second)
{
	int i = 0;
	for (; i < sizeof(data->russian) / sizeof(int); i++)
		data->russian[i] = calcfs(find_alpha(data, first[i]), find_alpha(data, second[i]));
}

#define uns(x) ((x < 0) ? (x += 961) : 0)

int gcd_func (int x, int temp)
{
	if (!temp)
		return (x);
		
	return gcd_func(temp, x % temp);
}	

void calculate_a(all_data *data, int x, int y, int min)
{
	uns(x);
	uns(y);
	min = gcd_func(x, 961);
	delete[] data->a;
	delete[] data->b;
	data->a = new int[min];
	data->b = new int[min];
	data->size_mas = min;
	for (int i = 0; i < data->size_mas; i++)
	{
		data->a[i] = (evklid(x, 961) * y);
		uns(data->a[i]);
		data->a[i] += i * 961;
		data->a[i] %= 961;
		uns(data->a[i]);
	}
}

void calculate_b(all_data *data, int i, int rus, int cand)
{
	for (; i < data->size_mas; i++)
	{
		(data->b[i] = (cand - data->a[i] * rus) % 961) && (uns(data->b[i]));
	}
}

int print_tmp(wchar_t *tmp)
{
	wcout << tmp << endl;
	exit (1);
}

#define add_one (cur = find_alpha(data, text[i]), count[cur] += 1)

double calc_index(wchar_t *text, int size, all_data *data, double &ret)
{
	int *count = new int[31]{0};
	int cur;
	for (int i = 0; i < size; i++)
	{
		add_one;
	}
	for (int i = 0; i < 31; i++)
	{
		double first = (double)((double)count[i] * ((double)count[i] - 1.0));
		double second = first / (double) (size * (size - 1));
		ret += second;
	}
	return (ret);
}

void check_text(all_data *data, int n)
{
	wchar_t *tmp = new wchar_t[data->file_size + 1];
	tmp[data->file_size] = n;
	int t = 0, conv, mod;
	double index;
	
	for (; t < data->size_mas; t++)
	{
		for (int i = 0; i < data->bigram_size; i++)
		{
			conv = evklid(data->a[t], 961);
			if (!conv)
				continue;
			
			conv *= (data->bigram_text[i] - data->b[t]);
			conv %= 961;
			uns(conv);
			
			mod = conv % 31;
			tmp[i * 2 + 1] = data->alp[mod];
			tmp[i * 2] = data->alp[(conv - mod) / 31];
		}
		index = 0;
		calc_index(tmp, data->file_size, data, index);
		wcout << "index for case = " << index << endl << endl;
		/* index for case = 0,0580259 */
		(index > 0.055) ? print_tmp(tmp) : 0;
	}
}

void check_variant(all_data *data, int i, int l, int j, int k)
{
	calc_a;
	wcout << "\na = " << data->a[0] << endl;
	calc_b;
	wcout << "b = " << data->b[0] << endl << endl;
	check_text(data, 0);
}

void combine(all_data *data)
{
	for (int i = 0; i < 5; i++)
	{
		for (int l = 0; l < 5; l++)
		{
			for (int j = 0; j < 5; j++)
			{
				for (int k = 0; k < 5; k++)
				{
					if (i == j || l == k)
						continue;

					check_variant(data, i, l, j, k);
				}
			}
		}
	}
}

void calc_best(all_data *data)
{
	int cur;
	int i = -1;
	bool used[961];
	for (int l = 0; l < sizeof used; l++)
		used[l] = false;
	
	for (; ++i < sizeof(data->best_cand) / sizeof(int);)
	{
		int best_cand = 0;
		int l = -1;
		for (; ++l < sizeof used;)
		{
			if (!used[l] && data->count_bigrams[l] > data->count_bigrams[best_cand])
				best_cand = l;
		}
		data->best_cand[i] = best_cand;
		used[best_cand] = true;

	}
	
	russian(data, L"снтне", L"тооан");
	wcout << "candidates\t\trussian\n";
	for (int l = 0; l < 5; l++)
	{
		wcout << data->best_cand[l] << "\t\t\t" << data->russian[l] << endl;
	}
	combine(data);
}

int convert_text(all_data *data)
{
	data->bigram_text = new int[data->file_size / 2];
	data->bigram_size = data->file_size / 2;
	data->count_bigrams = new int[data->size_alpha * data->size_alpha];
	for (int i = 0; i < data->size_alpha * data->size_alpha; i++)
		data->count_bigrams[i] = 0;
	
	bool first = false;
	unsigned int calc = 0;
	for (int i = 0; i < data->file_size; i+=1)
	{
		if (!first)
		{
			calc = 31;
			calc *= find_alpha(data, data->str[i]);
			first = true;
			continue;
		}
		
		first = false;
		calc += find_alpha(data, data->str[i]);
		data->count_bigrams[calc] += 1;
		if (calc > 961)
			return (0);
			
		data->bigram_text[i / 2] = calc;
	}
	calc_best(data);
	return (1);
}

int main(int argc, char **argv)
{
	all_data *data = new all_data;
	data->alp = L"абвгдежзийклмнопрстуфхцчшщыьэюя";
	data->size_alpha = 31;
	data->filename = "V12";
	data->file = wfstream(data->filename);
	setlocale(LC_ALL, "");
	wcout.imbue(locale(""));
	(data->file).imbue(locale(""));
	getline(data->file, data->str);
	wcout << "read " << data->str.size() << " letters, " << data->str.size() / 2 << " bigrams " << endl << endl;
	data->file_size = data->str.size();
	
	if (!convert_text(data))
		return (0);
	
	delete data;
	return (1);
}

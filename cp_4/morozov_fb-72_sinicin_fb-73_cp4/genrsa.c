#include <stdio.h>
#include <strings.h>
#include "gmp.h"
#include <time.h>
#include <math.h>
#include <stdlib.h>

typedef struct s_data
{
	gmp_randstate_t state;
	mpz_t		s;
	mpz_t		d;
	mpz_t		one;
	mpz_t		a;
	mpz_t		j;
	mpz_t		temp;
	mpz_t		n_min;
	mp_bitcnt_t	bits;
	mpz_t 		module;
    mpz_t 		pub;
    mpz_t 		priv;
	mpz_t 		first;
    mpz_t 		second;
    mpz_t 		maximum;
	int 		bit_of_1;
}	t_data;

#define SHORT_ARGS(x, y, z) (x),(x),(y),(z) 

void encrypt(mpz_t mes, mpz_t public_exp, mpz_t modulus)
{
	mpz_powm(SHORT_ARGS(mes, public_exp, modulus));
}

void decrypt(mpz_t mes, mpz_t private_exp, mpz_t modulus)
{
	mpz_powm(SHORT_ARGS(mes, private_exp, modulus));
}

void signature(mpz_t mes, mpz_t priv, mpz_t mod)
{
	mpz_powm(SHORT_ARGS(mes, priv, mod));
}

unsigned int verify(mpz_t mes, mpz_t pub, mpz_t mod, mpz_t copy)
{
	mpz_powm(SHORT_ARGS(mes, pub, mod));
	return (!mpz_cmp(mes, copy));
}

void init_data(t_data *data)
{
	mpz_init(data->first);
	mpz_init(data->second);
	gmp_randinit_mt(data->state);
	gmp_randseed_ui(data->state, time(NULL));
	mpz_init(data->maximum);
	mpz_urandomb(data->first, data->state, data->bit_of_1 - 1);
	mpz_urandomb(data->second, data->state, data->bit_of_1 - 1);
}

void make_nepar(t_data *data)
{
	mpz_setbit(data->first, data->bit_of_1 - 1);
	mpz_setbit(data->first, 0);
    mpz_setbit(data->second, data->bit_of_1 - 1);
	mpz_setbit(data->second, 0);
}

void get_maximum(t_data *data)
{
	mpz_set_str(data->maximum, "0", 10);
	int i = -1;
	while (++i < data->bit_of_1)
		mpz_setbit(data->maximum, i);
}

int	first_func(mpz_t n, t_data *data)
{
	mpz_urandomb(data->a, data->state, data->bit_of_1);
	mpz_setbit(data->a, data->bit_of_1 - 1);
	mpz_powm(data->a, data->a, data->d, n);
	mpz_set_str(data->j, "1", 10);
	return (!mpz_cmp_ui(data->a, 1) || !mpz_cmp(data->a, data->n_min));
}

int	get_check(mpz_t n, t_data *data)
{
	mpz_div_ui(data->n_min, n, 1);
    for (int i = 0; i < 10; i++)
    {
		if (first_func(n, data))
			continue;
			
        for (; mpz_cmp(data->j, data->s) < 0; mpz_add(data->j, data->j, data->one))
        {
            mpz_powm_ui(data->a, data->a, 2, n);
            if (!mpz_cmp(data->a, data->one))
                return 0;
			
            if (!mpz_cmp(data->a, data->n_min))
                break;
        }
        
        if (!mpz_cmp(data->j, data->s))
        	return 0;
    }
    return 1;

}

int	miller_rabin(mpz_t n, t_data *data)
{
	if (!mpz_cdiv_ui(n, 3) || !mpz_cdiv_ui(n, 5) || !mpz_cdiv_ui(n, 7) || !mpz_cdiv_ui(n, 11) || !mpz_cdiv_ui(n, 13))
       return 0;
       
	mpz_set_str(data->one, "1", 10);
	mpz_set_str(data->s, "0", 10);
	mpz_sub_ui(data->d, n, 1);
	for (; "continuing"; mpz_add_ui(data->s, data->s, 1), mpz_div_ui(data->d, data->d, 2))	
	{
		mpz_and(data->temp, data->d, data->one);
		if (mpz_cmp_ui(data->temp, 0) != 0)
			break ;
	}
	int ret = get_check(n, data);
	return ret;

}

void iterate(mpz_t cur, t_data *data)
{
	for(; mpz_cmp(cur, data->maximum) < 0; mpz_add_ui(cur, cur, 2))
	{
        if(miller_rabin(cur, data))
            break;
    }
}

void get_primes(t_data *data)
{
	mpz_init(data->j);
    mpz_init(data->s);
    mpz_init(data->d);
    mpz_init(data->temp);
    mpz_init(data->one);
    mpz_init(data->n_min);
    mpz_init(data->a);
	iterate(data->first, data);
	iterate(data->second, data);
	mpz_clear(data->s);
    mpz_clear(data->d);
    mpz_clear(data->one);
    mpz_clear(data->a);
    mpz_clear(data->j);
    mpz_clear(data->temp);
    mpz_clear(data->n_min);
}

void init_vars(t_data *data)
{
	mpz_init(data->module);
    mpz_init(data->pub);
    mpz_init(data->priv);
}

void calc_vars(t_data *data)
{
	mpz_set_str(data->pub, "10001", 16);
	mpz_mul(data->module1, data->first, data->second);
	mpz_t euler_mul;
	mpz_t euler1;
	mpz_t euler2;
	mpz_init(euler1);
	mpz_init(euler2);
	mpz_init(euler_mul);
	mpz_sub_ui(euler1, data->first, 1);
	mpz_sub_ui(euler2, data->second, 1);
	mpz_mul(euler_mul, euler1, euler2);
	mpz_invert(data->priv, data->pub, euler_mul);
	gmp_printf("first\nmodule:\t\t%Zx\npublic exp:\t%Zx\npriv exp:\t%Zx\n\n\n", data->module, data->pub, data->priv);
}

void go_magic_with_random_message(t_data *data)
{
	mpz_t msg;
    mpz_init(msg);
	mpz_t cp;
    mpz_init(cp);
    mpz_urandomb(msg, data->state, data->bit_of_1);
    mpz_set(cp, msg);
    gmp_printf("start: %Zx\n", msg);
    encrypt(msg, data->pub, data->module);
    gmp_printf("after encoding %Zx\n", msg);
    decrypt(msg, data->priv, data->module);
    gmp_printf("after decoding %Zx\n", msg);
	
	if (!mpz_cmp(msg, cp))
		printf("\nall fine\n");
		
    signature(msg, data->priv, data->module);
	gmp_printf("signed msg is %Zx\n\n", msg);
	
    if (verify(msg, data->pub, data->module, cp))
		printf("verifying done\n");
	else
		printf("verifying did not done\n");
}

int	main(int argc, char **argv)
{
	int num_bits;
	t_data *data = malloc(sizeof(t_data));
	if (argc != 2 || (num_bits = atoi(argv[1])) < 256)
	{
		printf("Use %s num_of_bits(256+)\n", argv[0]);
		return 0;
	}
	bzero(data, sizeof(t_data));
	data->bit_of_1 = num_bits / 2;
	init_data(data);
	make_nepar(data);
	get_maximum(data);
	get_primes(data);
	gmp_printf("\n1 - %Zd\n2 - %Zd\n\n", data->first, data->second);
	init_vars(data);
	calc_vars(data);
	go_magic_with_random_message(data);
	return 1;
}

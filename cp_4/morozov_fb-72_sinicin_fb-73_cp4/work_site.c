#include <stdio.h>
#include <stdlib.h>
#include "gmp.h"

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

void ReceiveKey(mpz_t pub, mpz_t Signature, mpz_t module_my, mpz_t Key, mpz_t private_exp, mpz_t module_site)
{
	decrypt(Key, private_exp, module_my);
	decrypt(Signature, private_exp, module_my);
	
	if (!verify(Signature, pub, module_site, Key)) 
	{
		printf("\nFailed\n");
		exit(1);
	}
}

void    SendKey(mpz_t pub, mpz_t Signature, mpz_t module_my, mpz_t Key, mpz_t private_exp, mpz_t module_site)
{
	signature(Signature, private_exp, module_my);
	encrypt(Signature, pub, module_site);
	encrypt(Key, pub, module_site);
}

int main(int argc, char **argv)
{
	char input[100];
	printf("Enter modulus from site\n");
	scanf("%s", input);
	
	mpz_t module_site;
	mpz_init(module_site);
	mpz_set_str(module_site, input, 16);
	
	printf("\nEnter Key from site\n");
	scanf("%s", input);
	
	mpz_t Key;
	mpz_init(Key);
	mpz_set_str(Key, input, 16);
	
	printf("\nEnter Signature from site\n");
	scanf("%s", input);
	
	mpz_t Signature;
	mpz_init(Signature);
	mpz_set_str(Signature, input, 16);
	
	printf("\nEnter your modulus\n");
	scanf("%s", input);
	
	mpz_t module_my;
	mpz_init(module_my);
	mpz_set_str(module_my, input, 16);
	printf("\nEnter your private exponent\n");
	scanf("%s", input);
	
	mpz_t pub, private_exp;
	mpz_init(pub);
	mpz_init(private_exp);
	mpz_set_str(private_exp, input, 16);
	mpz_set_str(pub, "65537", 10);
	
	ReceiveKey(pub, Signature, module_my, Key, private_exp, module_site);
	
	gmp_printf("\nVerificated | Key is %Zx\n", Key);
	printf("\nEnter your Key\n");
	scanf("%s", input);
	
	mpz_set_str(Key, input, 16);
	mpz_set(Signature, Key);
	SendKey(pub, Signature, module_my, Key, private_exp, module_site);
	gmp_printf("\nKey:\t\t%Zx\nSignature:\t%Zx\n", Key, Signature);
	return 0;
}

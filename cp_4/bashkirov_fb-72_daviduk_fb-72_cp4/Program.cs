using System;
using System.Text;
using System.Globalization;
using System.Numerics;

namespace ConsoleApp3
{
    class abonent
    {
        public abonent(BigInteger pub, BigInteger modulus)// конструктор от pub и module (используем его когда получаем публичный ключ сайта)
        {
            module = modulus;
            public_exp = pub;
        }
        public abonent()// просто конструктор по умолчанию
        {
            rand = new Random();
            generatedq = new BigInteger();
            generatedp = new BigInteger();
        }
        static private Random rand;// для рандома
        private BigInteger generatedq;// полученное после просто рандома p и q
        private BigInteger generatedp;
        private BigInteger q;// тут будем хранить уже простые p и q
        private BigInteger p;
        public BigInteger module { get; private set; }//тут хранится модуль абонента
        public BigInteger public_exp { get; private set; }//тут хранится публичная экспонента абонента
        public BigInteger private_exp { get; private set; }//тут хранится приватная экспонента абонента

        public void dump()// метод вывода
        {
            Console.WriteLine("p = " + p.ToString("x") + "\nq = " + q.ToString("x") +
                "\nmodule = " + module.ToString("x") + "\npublic exp = " +
                public_exp.ToString("x") + "\nprivate exp = " + private_exp);
        }

        private bool Miller_Rabin(BigInteger n, int bits)// проверка на простоту миллера рабина
        {
            // Write n-1 as d*2^s by factoring powers of 2 from n-1
            int s = 0;
            for (BigInteger m = n - 1; (m & 1) == 0; ++s, m >>= 1)
                ; // loop

            BigInteger d = (n - 1) / (new BigInteger(1) << s);

            for (int i = 0; i < 10; ++i)
            {
                BigInteger a = n - 2;// делаем копию n
                for (int l = 1; l < bits; l++)
                    if (rand.Next(0, 2) > 0)
                        a ^= (new BigInteger(1) << l);// случайно меняем биты a. в итоге у нас 2 < a < n - 2
                BigInteger x = BigInteger.ModPow(a, d, n);// modpow - встроенная функция нахождения поднесения в степень по модулю
                if (x == 1 || x == n - 1)
                    continue;
                for (int r = 1; r <= s - 1; ++r)
                {
                    x = BigInteger.ModPow(a, d, n);
                    if (x == 1) return false;
                    if (x == n - 1) goto LOOP;
                }

                return false;
            LOOP:
                continue;
            }

            // n is *probably* prime
            return true;
        }
        private BigInteger get_next_prime(BigInteger n, int bits)
        {
            BigInteger i;
            for (i = n; !Miller_Rabin(i, bits); i += 2)// пока не наткнемся на простое число - добавляем по 2
                ;
            return (i);
        }

        public void generatepq(int size_key)// тут генерируем p и q
        {
            int half_key = size_key / 2;
            for (int i = 1; i < half_key - 1; i++)
            {
                if (rand.Next(0, 2) == 0)
                    generatedq |= (new BigInteger(1) << i);// ставим случайные биты
                if (rand.Next(0, 2) == 0)
                    generatedp |= (new BigInteger(1) << i);
            }
            generatedq += 1;// делаем число непарным
            generatedp += 1;
            p = get_next_prime(generatedp, half_key);// начинаем из згенерированных случайных чисел получать простые
            q = get_next_prime(generatedq, half_key);
            Console.WriteLine("p and q generated");
        }
        public void calculate_keys()
        {
            create_module();
            create_pub();
            create_priv();
        }
        private void create_module()
        {
            module = p * q;// ну тут понятно
        }

        private void create_pub()
        {
            public_exp = 65537;// тут ставим 65537, хотя можно и згенерировать другое
        }

        static BigInteger modInverse(BigInteger a, BigInteger n)// функция нахождения обратного по модулю
        {
            BigInteger i;
            BigInteger v = 0;
            BigInteger d = 1;
            BigInteger x;
            for (i = n;  a > 0; v = x)
            {
                x = a;
                BigInteger t = i / a;
                a = i % x;
                i = x; 
                x = d;
                d = v - t * x;
            }
            v %= n;
            v = ((v < 0) ? (v = (v + n) % n) : v);
            return v;
        }
        private void create_priv()
        {
            BigInteger euler = (p - 1) * (q - 1);// умножаем 2 числа ейлера для p и q
            private_exp = modInverse(public_exp, euler);// находим обратный по модулю для public_exp. это закрытый ключ
        }

        public BigInteger encrypt(BigInteger Message)
        {
            return BigInteger.ModPow(Message, public_exp, module);// так зашифровываем
        }
        public BigInteger decrypt(BigInteger CypherText)
        {
            return BigInteger.ModPow(CypherText, private_exp, module);// так разшифровываем
        }
        public BigInteger Signature(BigInteger Message)
        {
            return BigInteger.ModPow(Message, private_exp, module);// так делаем подпись
        }
        public bool verify(BigInteger Sign, BigInteger for_verifying)
        {
            BigInteger designed = BigInteger.ModPow(Sign, public_exp, module);// а так проверяем на соответствие подписи
            return (designed == for_verifying);
        }
        public void receive_key()// тут протокол получения ключа для более быстрой симметричной криптографии
        {
            // http://asymcryptwebservice.appspot.com/?section=rsa
            Console.WriteLine("Enter modulus from site");// вводим тут модуль из вкладки server key
            BigInteger site_modulus = BigInteger.Parse("00" + Console.ReadLine(), NumberStyles.AllowHexSpecifier);
            // заходим на вкладку send key
            Console.WriteLine("Enter Key from site");// вводим ключ из сайта
            BigInteger key = BigInteger.Parse("00" + Console.ReadLine(), NumberStyles.AllowHexSpecifier);// добавляем нули в начало, иначе C#- ный интегер начинает делать дичь.
            Console.WriteLine("Enter signature from site");
            BigInteger signature = BigInteger.Parse("00" + Console.ReadLine(), NumberStyles.AllowHexSpecifier);//вводим signature из вкладки Send Key
            key = decrypt(key);// декриптим ключ из сайта нашим ключом
            signature = decrypt(signature);// декриптим сигнатуру нашим ключом
            abonent site = new abonent(65537, site_modulus);// делаем нового виртуального абонента для сайта. у него будет только модуль и паблик ключ
            if (site.verify(signature, key))// проверяем совпадает ли подпись с ключом
                Console.WriteLine("Verification Success");
            else
                Console.WriteLine("Verification Failed");
            Console.WriteLine("Key = " + key);// выводим ключ
        }
        public void send_key()// здесь отправляем уже мы
        {
            // http://asymcryptwebservice.appspot.com/?section=rsa
            Console.WriteLine("Enter modulus from site");// вводим тут модуль из вкладки server key
            BigInteger site_modulus = BigInteger.Parse("00" + Console.ReadLine(), NumberStyles.AllowHexSpecifier);
            Console.WriteLine("Enter Key to send");// вводим тут наш для симметричной криптографии, небольшой длины
            BigInteger msg = BigInteger.Parse("00" + Console.ReadLine(), NumberStyles.AllowHexSpecifier);
            BigInteger Sign = msg;
            Sign = Signature(Sign);// подписываем ключ для симметричной криптографии нашим ключом
            abonent site = new abonent(65537, site_modulus);// опять делаем вирт. абонента
            Sign = site.encrypt(Sign);// зашифровываем подписанный ключ
            msg = site.encrypt(msg);// зашифровываем ключ
            Console.WriteLine("Key = " + msg.ToString("x"));// это нужно будет вводить в вкладку receive key
            Console.WriteLine("Signature is " + Sign.ToString("x"));// это тоже
            // а еще туда нужно будет вводить наш модуль и публичный ключ, публичный ключ выводится в самом начале, после генерации
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            abonent a = new abonent();// создаем обьекты класса абонент
            abonent b = new abonent();
            a.generatepq(256);// генерируем p и q чтобы получилось в модуле 256 бит.
            a.calculate_keys();// считаем модуль, ставим публичную экспоненту 65537, считаем приватный ключ
            a.dump();// выводим все переменные
            b.generatepq(256);
            b.calculate_keys();
            b.dump();
            BigInteger msg = BigInteger.Parse("11123213");// берем какое-то число в качестве сообщения, начинаем с ним играть
            BigInteger copy = msg;// получаем копию
            Console.WriteLine(msg.ToString("x"));
            msg = a.encrypt(msg);// зашифровываем 
            Console.WriteLine(msg.ToString("x"));
            msg = a.decrypt(msg);// разшифровываем
            Console.WriteLine(msg.ToString("x"));
            msg = b.Signature(msg);// подписываем абонентом b
            Console.WriteLine(msg.ToString("x"));
            Console.WriteLine(b.verify(msg, copy));// проверяем подпись с его копией. если вывело true - все хорошо
            a.receive_key();// запускаем работу с сайтом. получаем ключ.
            a.send_key();//отправляем ключ.
        }
    }
}

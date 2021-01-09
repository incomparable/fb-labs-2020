import java.lang.Math.*
import java.math.BigInteger
import java.util.concurrent.ThreadLocalRandom
import kotlin.experimental.or
import kotlin.math.pow
import kotlin.random.Random
import kotlin.random.Random.Default.nextInt
import kotlin.random.asJavaRandom

//pre-Operations
val firstPrimes = ArrayList<BigInteger>().also {
    val firstPrimesString = "2\t3\t5\t7\t11\t13\t17\t19\t23\t29\t31\t37\t41\t43\t47\t53\t59\t61\t67\t71\t73\t79\t83\t89\t97\t101\t103\t107\t109\t113\t127\t131\t137\t139\t149\t151\t157\t163\t167\t173\t179\t181\t191\t193\t197\t199\t211\t223\t227\t229\t233\t239\t241\t251\t257\t263\t269\t271\t277\t281\t283\t293\t307\t311\t313\t317\t331\t337\t347\t349\t353\t359\t367\t373\t379\t383\t389\t397\t401\t409\t419\t421\t431\t433\t439\t443\t449\t457\t461\t463\t467\t479\t487\t491\t499\t503\t509\t521\t523\t541"
    for (each in firstPrimesString.splitToSequence('\t')) {
        it.add(each.toBigInteger())
    }
}
val zero = 0.toBigInteger()
val one = 1.toBigInteger()

tailrec fun gcd(x: BigInteger, y: BigInteger): BigInteger {
    if (y == zero) {
        return x
    }
    return gcd(y, x % y)
}//OK

fun evklidExpansed(x: BigInteger, y: BigInteger): List<BigInteger> {


    if (x == zero) {
        return listOf(y, zero, one)
    }
    val (d, xx, yy) = evklidExpansed(y % x, x)
    return listOf(d, yy - (y / x) * xx, xx)

}//OK

fun inversedBModule(number: BigInteger, module: BigInteger): BigInteger {
    var evkExp = evklidExpansed(number, module)
    if (evkExp[0] == one) {
        var numbr = evkExp[1]%module
        if(numbr < zero ) {
            numbr +=module
        }
        return numbr
    } else {
        print("There's no inversion for this number by such module")
    }
    return zero
} //OK

fun bigIntegerGenerator(bitLength: Int): BigInteger {

//    val length = bitLength / 8
//    val shift = bitLength % 8
//    val randomByteStuff = if (shift != 0) {
//        var randomByteStuff = Random.nextBytes(length + 1)
//        var endByte = (randomByteStuff[1].toInt() shr (7 - shift))
//        val lastBit = 2.0.pow(endByte.toDouble()).toInt()
//        endByte = endByte or lastBit
//        randomByteStuff[0] = 0
//        randomByteStuff[1] = endByte.toByte()
//        randomByteStuff[randomByteStuff.size - 1] = randomByteStuff[randomByteStuff.size - 1] or 1
//        randomByteStuff
//    } else {
//        val randomBS = Random.nextBytes(length + 1)
//        randomBS[0] = 0
//        randomBS[1] = randomBS[1] or 128.toByte()
//        randomBS[randomBS.size - 1] = randomBS[randomBS.size - 1] or 1
//        randomBS
//    }
//
//    return ((BigInteger(randomByteStuff)).abs())
    return BigInteger(bitLength, Random.asJavaRandom())
} //OK

fun simpleCheck(integer: BigInteger): Boolean {
    for (each in firstPrimes) {
        if (integer % each == zero) {
            return false
        }
    }
    return true
}//OK

fun power(number: BigInteger, pw: BigInteger, module: BigInteger): BigInteger {
    /*
    var tempNumber = number
    var answer = one
    val byteList = pw.toByteArray()

    for (byte in byteList) {
        for (i in 0..7) {
            val b = (byte.toInt() shr i) and 1
            if (b == 1) {
                answer = (tempNumber * answer) % module
            }
            tempNumber = tempNumber.pow(2) % module
        }
    }
    return answer*/
    return number.modPow(pw, module)
} //OK

fun millerCheck(integer: BigInteger): Boolean {



    val probPrime = integer - one
    var d = probPrime
    var counter = zero

    while(d%2.toBigInteger() == zero){
        d /= 2.toBigInteger()
        counter++
    }

    for (i in 1..100) {
        var rnd = Random.asJavaRandom()

        var x = BigInteger(integer.bitLength(), rnd)
        while(x<=one || x>=integer){
                x = BigInteger(integer.bitLength(), rnd)
        }

        var forIterations = zero
        var xr = x.modPow(d, integer)
        while (!(forIterations == zero && xr == one || xr == probPrime)) {
            if (forIterations > zero && xr == one || forIterations+one == counter ) {
                return false
            }
            forIterations++
            xr = xr.modPow(2.toBigInteger(), integer)
        }
    }
    return true
}

fun createPrime(length: Int): BigInteger {

    val badKeys = ArrayList<BigInteger>()

    while (true) {
        var big = bigIntegerGenerator(length)
        while(!simpleCheck(big)){
            big = bigIntegerGenerator(length)
        }
        if (millerCheck(big)){
            for(each in badKeys){
                println("There was a bad key during bigprime generation: ${each}")
            }
            return big
        }else {
            badKeys.add(big)
        }
    }
}

fun generateKeyPair(length: Int):Pair<BigInteger, BigInteger>{
    val a = createPrime(length)
    val b = createPrime(length)
    return  a to b
} // OK

fun generateUserKeys(length: Int): ArrayList<List<BigInteger>>{

    var check = true
    val pairs = ArrayList<Pair<BigInteger, BigInteger>>()

    while (check){
        val (p, q) = generateKeyPair(length)
        val (p1, q1) = generateKeyPair(length)
        if(p*q <= p1*q1){
            check = false
            pairs.add(p to q)
            pairs.add(p1 to q1)
        }
    }

    val keys = ArrayList<List<BigInteger>>()

    for (each in pairs){
        val p = each.first
        val q = each.second
        val n = p*q
        val e = 65537.toBigInteger()
        val d = inversedBModule(e, euiler(p, q))
        if(d == zero){
            println("    ksdgkk    ")
        }
        keys.add(listOf(p, q, n, e, d))
    }

//    if (keys[0][4] == zero || keys[1][4] == zero){
//        return generateUserKeys(length)
//    }
    return keys
}//OK

fun euiler(p: BigInteger, q: BigInteger): BigInteger{
    return (p-one) * (q-one)
}//OK

//RSA

fun encryption(message: BigInteger, e: BigInteger, n: BigInteger):BigInteger{
    return power(message, e, n)
}
fun decryption(encryptedMessage: BigInteger, d: BigInteger, n: BigInteger):BigInteger{
    return power(encryptedMessage, d, n)
}
fun signMessage(sign: BigInteger, d: BigInteger, n: BigInteger):BigInteger{
    return  power(sign, d, n)
}
fun verifyMessage(message: BigInteger, s: BigInteger, e1: BigInteger, n1: BigInteger):Boolean{
    return message == power(s, e1, n1)
}
fun sendKey(Receiver: User, Sender: User){
    val s = signMessage(Sender.message, Sender.d, Sender.n)
    Receiver.message  = encryption(Sender.message, Receiver.e, Receiver.n)

    println("Sender's message: ${Sender.message}, encrypted message: ${Receiver.message}")
    println("The sign is: ${s}")

    Receiver.sign = encryption(s, Receiver.e, Receiver.n)
    println("Encrypted sign is: ${Receiver.sign}")
}
fun receiveKey(Receiver: User, Sender: User):Boolean{
    Receiver.message = decryption(Receiver.message, Receiver.d, Receiver.n)

    println("Decrypted message: ${Receiver.message}")

    Receiver.sign = decryption(Receiver.sign, Receiver.d, Receiver.n)

    println("Verifying sign; the sign is: ${Receiver.sign}")

    return verifyMessage(Receiver.message, Receiver.sign, Sender.e, Sender.n)
}


data class User(
        val name: String,
        var p: BigInteger,
        var q: BigInteger,
        var n: BigInteger,
        var e: BigInteger,
        var d: BigInteger,
        var sign: BigInteger,
        var message: BigInteger
    )

tailrec fun main() {

    println()

    val messages = ArrayList<BigInteger>()

    val messageA = nextInt(1, 160).toBigInteger()
    val messageB = nextInt(1, 160).toBigInteger()

    messages.add(messageA)
    messages.add(messageB)

    val users = ArrayList<User>()

    users.add(User("Alice", zero, zero, zero, zero, zero, zero, zero))
    users.add(User("Bob", zero, zero, zero, zero, zero, zero, zero))

    val keys = generateUserKeys(256)
    for((key, user) in keys.zip(users)){
        user.p = key[0]
        user.q = key[1]
        user.n = key[2]
        user.e = key[3]
        user.d = key[4]
        user.sign = zero
    }
    for((message, user) in messages.zip(users)){
        user.message = message
    }

    println("Information about users:")
    for(usr in users){
        println("Name -${usr.name} Message - ${usr.message},d - ${usr.d}, e - ${usr.e}, n - ${usr.n} , q - ${usr.q}, p - ${usr.p}, sign - ${usr.sign}")
    }


    //starting messaging
    val (Alice, Bob) = users
    sendKey(Alice, Bob)
    val check = receiveKey(Alice, Bob)
    if(check){
        println("message exchanging successful, sign verified")
    } else{
        println("Theres an error, the keys are mistaken(probably miller check wasnt strong enough")
    }

   if(!check){
       main()
   }
    //modulus: 5F46182B368ACF36FCC5E4639286BE84EE92561254CAA4C60D1C330059AC9CBD742E2B66D159EE2ED40A1F437540A1953BEC7338E3E905699F96B9F46C0FFC2F
    //modulus: 5f46182b368acf36fcc5e4639286be84ee92561254caa4c60d1c330059ac9cbd742e2b66d159ee2ed40a1f437540a1953bec7338e3e905699f96b9f46c0ffc2f
    //public exponent: 10001
    //ciphertext: 55D304D9DD092356610FC3D21107045D021442ABAA2F59C195A277BBF7D141A27E2D8B578BB626B8A9F33C52390AC0829FE56F3573C6291877FC9313AC1FE650
    //sign: ACF03E50DAA13AE3298A7551CF711FC793773B89EBF691F3D225E9A8BA42DF7C
}




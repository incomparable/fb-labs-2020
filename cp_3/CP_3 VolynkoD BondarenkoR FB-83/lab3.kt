import java.io.FileReader
import java.io.FileWriter
import java.lang.Exception
import java.lang.IllegalArgumentException
import java.lang.Math.floorMod
import kotlin.math.abs

val popChar = "оеаинт"
val mostUsedRusBigrams = listOf("ст", "но", "то", "на", "ен")
const val alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
val module = alphabet.length


fun evklidExpansed(x: Int, y: Int): List<Int> {

    if (x == 0) {
        return listOf(y, 0, 1)
    }
    val (d, xx, yy) = evklidExpansed(Math.floorMod(y, x), x)

    return listOf(d, yy - (y / x) * xx, xx)

} //OK

fun conversed(number: Int, module: Int): Int {

    var numbr = number % module
    if (numbr < 0) {
        numbr += module
    }
    val (d, x, y) = evklidExpansed(numbr, module)

    if (d == 1) {
//        if (x < 0) {
//            return x + module
//        } else {
            return x
//        }
    } else {
        //       print("There's no inversion for this number by such module")
        return 0
    }
    return 0
} //OK

fun equation(x: Int, y: Int, md: Int): List<Int> {
    var answers = ArrayList<Int>()
    var dilnik = Math.floorMod(evklidExpansed(x, md).elementAt(0), md)

    if (dilnik == 1) {
        val x_c = Math.floorMod((conversed(x, md) * y), md)
        answers.add(x_c)
        return answers
    } else if (dilnik > 0) {
        if (Math.floorMod(y, dilnik) == 0) {
            var parameters = listOf(x / dilnik, y / dilnik, md / dilnik)
            var nDil = equation(parameters[0], parameters[1], parameters[2])[0]

            for (variables in 0 until dilnik) {
                val answer = nDil + variables * parameters.elementAt(2)
                answers.add(answer)

            }
            return answers
        } else {
            answers.add(0)
            return answers
        }
    }
    return emptyList()
}//OK

fun mostUsedBigrams(text: String): List<String> {
    var bigramsList = HashMap<String, Int>().also {
        for (st in text.chunked(2)) {
            var count = it[st] ?: 0
            it[st] = count + 1
        }
    }


    return bigramsList.asSequence()
        .sortedBy { it.value }
        .toList()
        .takeLast(5)
        .map { it.key }
        .reversed()

}//OK

fun isVariable(list:List<String>) {
    val(text, a, b) = list
    var frequences = HashMap<Char, Int>().also {
        for (letter in text) {
            var count = it[letter] ?: 0
            it[letter] = count + 1
        }
    }
    var textTopChars = frequences.asSequence()
        .sortedBy { it.value }
        .map { it.key }
        .toList()
        .reversed()
        .take(6)

    val str = textTopChars.joinToString("").toSortedSet()
    val str1 = popChar.toSortedSet()
    if(str == str1){
        println("$text \n Key was: $a , $b")

    }

}//OK

fun findKey(X: String, Y: String, XX: String, YY: String): ArrayList<Pair<Int, Int>> {
    val x = alphabet.indexOf(X[0]) * module + alphabet.indexOf(X[1])
    val y = alphabet.indexOf(Y[0]) * module + alphabet.indexOf(Y[1])
    val xx = alphabet.indexOf(XX[0]) * module + alphabet.indexOf(XX[1])
    val yy = alphabet.indexOf(YY[0]) * module + alphabet.indexOf(YY[1])

    val keys = ArrayList<Pair<Int, Int>>()

    val a = equation(x - xx, y - yy, module * module)
    for (each in a) {
        val b = Math.floorMod(y - x * each, module * module)
        keys.add(each to b)
    }
    return keys
}

fun numToBigram(Num: Int): String {
    val first = Num / module
    val second = Num % module
    return alphabet[first].toString() + alphabet[second]
}//OK

fun desipherFText(A: Int, B: Int, text: String): List<String> {
    val a = A
    val b = B
    var dText = ""
//    if(a == 654 && b == 777) {
//        println("654 and 777")}
//    else if(a == 777 && b == 654){
//        println("777 and 654")
//        }
//    else return "blya"
    for (bigram in text.chunked(2)) {
        if (bigram.length == 1) break

        var y = alphabet.indexOf(bigram[0]) * module + alphabet.indexOf(bigram[1])
//        if (y == 315 && a == 654 && b == 777){
//            println("start is ok")
//            return ""
//        }

        var aConversed = conversed(a, module * module)
        var c1 = y - b
        var num1 = Math.floorMod(c1 * aConversed, module * module)
//        if (num1 < 0) {
//            num1 += module * module
//        }
        dText += numToBigram(num1)
//        if(dText == "убивать"){
//            println("fafafaf")
//        }
//        if (dText.length >10)return ""
//
//    }
//    if(dText[0] == 'а' && dText[2] =='а' && dText[2] == 'а') {                       //
//        println(a)                                                                   //  for debugging
//        println(b)                                                                   //
//    }
    }
    return listOf(dText, a.toString(), b.toString())
}
//OK
fun decrypt(rusBigrams: List<String>, textBigrams: List<String>, text: String) {
    for (X in rusBigrams) {
        for (Y in textBigrams) {
            for (XX in rusBigrams) {
                for (YY in textBigrams) {
                    if (X == XX || Y == YY) continue


//                    val x = alphabet.indexOf(X[0])*module + alphabet.indexOf(X[1])
//                    val y = alphabet.indexOf(Y[0])*module + alphabet.indexOf(Y[1])

                    val keys = findKey(X, Y, XX, YY)
                    if (keys.isEmpty()) continue
                    for (each in keys) {
                        if (each.first == 0) continue
                        val (a, b) = each
//                        val aConv = conversed(a, module * module) //+ module*module
//                        if (aConv == 0) continue


//                        if(a == 654 && b == 777){
//                        isVariable(desipherFText(a, b, text))
//                        }
                        isVariable(desipherFText(a, b, text))
                    }
                }
            }
        }
    }
}



fun main() {

    var input = FileReader("E:/fb-labs-2020/cp_3/text.txt", charset("utf-8"))
        .buffered()
        .readText()
        .replace('ё', 'e')
        .replace('ъ', 'ь')
        .replace("\r\n", "")

    val bigramsFromText = mostUsedBigrams(input)

    println("П'ять найчастіших біграмм")
    for (each in bigramsFromText){
        println(each)
    }
    println()

    decrypt(mostUsedRusBigrams, bigramsFromText, input)

//    val output = FileWriter("E:/fb-labs-2020/cp_3/decr.txt")
//    val (text,a,b) = desipherFText(654, 777, input)
//    output.write(text)
//    output.close()
}
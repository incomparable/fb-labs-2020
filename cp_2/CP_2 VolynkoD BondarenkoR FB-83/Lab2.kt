import java.io.FileReader
import java.io.FileWriter

const val alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

fun index(text: String): Double {
    val frequency = HashMap<Char, Int>().also {
        for (letter in text) {
            val count = it[letter] ?: 0
            it[letter] = count + 1
        }
    }
    var cIndex = 0.0
    for (letter in frequency) {
        cIndex += (letter.value.toDouble() * (letter.value.toDouble() - 1))
    }
    return cIndex / ((text.length.toDouble()) * (text.length.toDouble() - 1))
}//OK

fun findKeyLength() {
    println("Надем длину ключа по индексам соответствия:")
    val decypheredText = FileReader("E:/fb-labs-2020/cp_2/DecriptionText.txt", charset("utf-8"))
        .buffered()
        .readText()
    val indices = DoubleArray(30)
    for (n in 2..31) {
        var ttext = ArrayList<Char>()
        for (letter in 1 until decypheredText.length) {
            if (letter % n == 0) {
                ttext.add(decypheredText[letter])
            }
        }
        indices[n - 2] = index(ttext.joinToString(""))

    }
    for (n in indices.indices) {
        println("r = ${n + 2}, Индекс соответствия - ${indices[n]};")
    }
}//OK

fun findKey(text: String) {
    println("Введите длину ключа по индексу соответствия: ")

    val keyLength = readLine()!!.toInt()
    val popularCharacters = "оеаинстр"
    val occurrence = ArrayList<Pair<Char, Int>>()
    val map = HashMap<Char, Int>()
    val sequences = ArrayList<String>()

    for (seqSymbol in 0 until keyLength) {
        val str = text.filterIndexed { index, _ -> index % keyLength ==  seqSymbol  }
        sequences.add(str)
    }

    for (sequence in sequences) {
        map.clear()
        for (letter in sequence.asSequence()) {
            val count = map[letter] ?: 0
            map[letter] = count + 1
        }
        occurrence.add(map.maxByOrNull { it.value }!!.toPair())
    }
    println(occurrence)
    for (popularChar in popularCharacters) {
        print("For $popularChar :")
        for (each in occurrence) {

            print("${alphabet[((alphabet.indexOf(each.first) - alphabet.indexOf(popularChar) + alphabet.length) % alphabet.length)]}")
        }
        println()
    }
}

fun decipher(text: String) {
    println("Введите ключ:")
    val Key = readLine()!!
    val decipheredText = CharArray(text.length)
    val cipherString = CharArray(text.length).also {
        for (symbol in text.indices) {
            it[symbol] = Key[symbol % (Key.length)]
        }
    }
    for (letter in text.indices) {
        decipheredText[letter] =
            alphabet[((alphabet.indexOf(text[letter]) - alphabet.indexOf(cipherString[letter]) + alphabet.length) % alphabet.length)]
    }
    println(decipheredText)
    val output = FileWriter("E:/fb-labs-2020/cp_2/DencriptionText.txt")
    output.write(decipheredText)
    output.close()
    var textN = ""
    for (each in decipheredText){
        textN += each.toString()
    }
    println(
        "Индекс соответствия дли шифрованого текста 5-го варианта - ${index(text)}, расшифрованого - ${index(textN)}"
    )
}//OK

fun encryption(word: String, alphabet: String, input: String) {
    val forI = index(input)
    var arrayO = ""
    val dA = CharArray(input.length).also {
        for (a in 0 until input.length) {
            it[a] = word[a % (word.length)]
        }
    }
    for ((i, n) in input.withIndex()) {
        val bukva =
            alphabet[(alphabet.indexOf(dA[i]) + alphabet.indexOf(n)) % (alphabet.length - 1)]
        arrayO += bukva.toString()
    }
    val forII = index(arrayO)
    val output = FileWriter("E:/fb-labs-2020/cp_2/EncriptionTextR${word.length}.txt")
    output.write(arrayO)
    output.close()
    println("Индекс соотвествия ВТ - ${forI}, Индекс соотвествия ШТ - $forII")
}//OK

fun main() {
    var input = FileReader("E:/fb-labs-2020/cp_2/EncriptionText.txt", charset("utf-8"))
        .buffered()
        .readText()
        .replace("ё", "е")
        .replace(" ","")




    input = clearText(input)
    encryption("ты", alphabet, input)
    encryption("тык", alphabet, input)
    encryption("тыкв", alphabet, input)
    encryption("тыква", alphabet, input)
    encryption("тыквасиделав", alphabet, input)
    input = FileReader("E:/fb-labs-2020/cp_2/DecriptionText.txt", charset("utf-8"))
        .buffered()
        .readText()
        .replace("ё", "e")

    findKeyLength()
    findKey(input)
    decipher(input)
}
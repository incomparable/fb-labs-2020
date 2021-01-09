import java.io.FileReader
import kotlin.collections.HashMap
import kotlin.math.log
import kotlin.math.log2

//const val alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя "

//val allowed = 'а'..'я'

fun clearText(text: String): String = text
    .toLowerCase()
    .replace('ъ', 'ь')
    .replace('ё', 'е')
    .replace('\n', ' ')
    .replace(Regex("[^а-я ]"), "")
    .replace(Regex(" +"), " ")

fun frequency(text: String) = text
    .groupingBy { it }
    .eachCount()
    .mapValues { it.value / text.length.toDouble() }
    .asSequence()
    .sortedByDescending { it.value }

fun monogramEnthropy(text: String) {
    var enthropy = 0.0
    var monogram = HashMap<Char, Double>().also {
        for (letter in text) {
            var count = it[letter] ?: 0.0
            it[letter] = count + 1.0
        }
        for (v in it) {
            v.setValue(v.value / text.length.toDouble())
        }
    }
    for (frequency in monogram) {
        enthropy += frequency.value * log2(frequency.value)
    }
    println("Энтропия для H(1) - ${enthropy * (-1)}, Избыточность - ${1 + (enthropy / log(32.0, 2.0))}")
}

fun monogramWithoutSpaces(text: String) {
    val textp = text.replace(" ", "")
    var enthropy = 0.0
    var monogram = HashMap<Char, Double>().also {
        for (letter in textp) {
            var count = it[letter] ?: 0.0
            it[letter] = count + 1.0
        }
        for (v in it) {
            v.setValue(v.value / textp.length.toDouble())
        }
    }
    for (frequency in monogram) {
        enthropy += frequency.value * log2(frequency.value)
    }
    println("Энтропия для H(1) тексте без пробелов - ${enthropy * (-1)}, Избыточность - ${1 + (enthropy / log( 31.0, 2.0))}")
}

fun entrophyB(bigrams: Map<String, Double>, itsCount: Int) {
    var enthropy = 0.0
    for (bigram in bigrams) {
        if (bigram.value == 0.0) {
            continue
        }
        val frequency = bigram.value / itsCount.toDouble()
        enthropy += frequency * kotlin.math.log(frequency, 2.0) / 2
    }
    enthropy = enthropy * (-1)
    println("Энтропия биграмм - $enthropy, Избыточность - ${1 - enthropy / log(32.0, 2.0)}")
}

fun entrophyBNoSpaces(bigrams: Map<String, Double>, itsCount: Int) {
    var enthropy = 0.0
    for (bigram in bigrams) {
        if (bigram.value == 0.0) {
            continue
        }
        val frequency = bigram.value / itsCount.toDouble()
        enthropy += frequency * kotlin.math.log(frequency, 2.0) / 2
    }
    enthropy = enthropy * (-1)
    println("Энтропия биграмм в тексте без пробелов - $enthropy, Избыточность - ${1 - enthropy / log(31.0, 2.0)}")
}

fun printingBigrams(bigrams: Map<String, Double>, withSpaces: Boolean) {
    if (withSpaces) {
        for (firstS in alphabet)
            for (secondS in alphabet) {
                print(" ${bigrams["$firstS$secondS"]}")
                if (secondS != alphabet[alphabet.length - 1]) {
                    print("\t")
                } else {
                    print("\n")
                }
            }
    } else {
        for (firstS in alphabet.replace(" ", ""))
            for (secondS in alphabet.replace(" ", "")) {
                print(" ${bigrams["$firstS$secondS"]}")
                if (secondS != alphabet[alphabet.length - 2]) {
                    print("\t")
                } else {
                    print("\n")
                }
            }
    }
}

fun bigramsEnthropy(text: String) {

    var counter1 = 0
    val bigramsC = HashMap<String, Double>().also {
        for (frst in alphabet) {
            for (scnd in alphabet) {
                it[frst.toString() + scnd.toString()] = 0.0
            }
        }

        for ((first, second) in text.zipWithNext()) {
            val f = first.toString()
            val s = second.toString()
            val count = it[f + s] ?: 0.0
            it[f + s] = count + 1.0
            counter1++
        }
    }
    var counter2 = 0
    val bigramsNC = HashMap<String, Double>().also {
        for (frst in alphabet) {
            for (scnd in alphabet) {
                it[frst.toString() + scnd.toString()] = 0.0
            }
        }

        for (pair in text.chunked(2)) {
            if (pair.length == 1) {
                break
            }
            val f = pair[0].toString()
            val s = pair[1].toString()
            val count = it[f + s] ?: 0.0
            it[f + s] = count + 1.0
            counter2++
        }
    }

    var counter3 = 0
    val bigramsNoSpacesC = HashMap<String, Double>().also {
        for (frst in alphabet.replace(" ", "")) {
            for (scnd in alphabet.replace(" ", "")) {
                it[frst.toString() + scnd.toString()] = 0.0
            }
        }

        for ((first, second) in text.replace(" ", "").zipWithNext()) {
            val f = first.toString()
            val s = second.toString()
            val count = it[f + s] ?: 0.0
            it[f + s] = count + 1.0
            counter3++
        }
    }
    var counter4 = 0
    val bigramsNoSpacesNC = HashMap<String, Double>().also {
        for (frst in alphabet.replace(" ", "")) {
            for (scnd in alphabet.replace(" ", "")) {
                it[frst.toString() + scnd.toString()] = 0.0
            }
        }

        for (pair in text.replace(" ", "").chunked(2)) {
            if (pair.length == 1) {
                break
            }
            val f = pair[0].toString()
            val s = pair[1].toString()
            val count = it[f + s] ?: 0.0
            it[f + s] = count + 1.0
            counter4++
        }
    }

    println("Пересекающиеся биграммы с пробелами:")
    printingBigrams(bigramsC, true)
    println("\n")
    println("Непересекающиеся биграммы с пробелами:")
    printingBigrams(bigramsNC, true)
    println("\n")

    println("Пересекающиеся биграммы без пробелов:")
    printingBigrams(bigramsNoSpacesC, false)
    println("\n")
    println("Непересекающиеся биграммы без пробелов:")
    printingBigrams(bigramsNoSpacesNC, false)
    println("\n")

    entrophyB(bigramsC, counter1)
    entrophyB(bigramsNC, counter2)
    entrophyBNoSpaces(bigramsNoSpacesC, counter3)
    entrophyBNoSpaces(bigramsNoSpacesNC, counter4)
}


fun main() {

    val input = clearText(
        FileReader("E:/fb-labs-2020/cp_1/TEXT.txt")
            .buffered()
            .readText()
    )

    println("With spaces:")
    for (each in frequency(input)) {
        println("${each.key} - ${each.value}")
    }
    println("Without spaces:")
    for (each in frequency(input.replace(" ",""))) {
        println("${each.key} - ${each.value}")
    }

    monogramEnthropy(input)
    monogramWithoutSpaces(input)


    bigramsEnthropy(input)

}


package chernrina.flight_db

import java.security.MessageDigest

fun String.sha512_5(login: String): String {
    var res=this
    res = "%s%s%s".format(login,res,"coursework")
    for (i in 0..9){
        res=hashString(res, "SHA-512")
    }
    return res
}

private fun hashString(input: String, algorithm: String): String {
    return MessageDigest
        .getInstance(algorithm)
        .digest(input.toByteArray())
        .fold("", { str, it -> str + "%02x".format(it) })
}

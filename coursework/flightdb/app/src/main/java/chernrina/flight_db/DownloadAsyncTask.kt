package chernrina.flight_db

import android.os.AsyncTask
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.URL
import java.net.URLConnection

class DownloadAsyncTask :  AsyncTask<String, Void, String>() {

    override fun doInBackground(vararg urls: String): String {
        var out = ""
        val url = URL(urls[0])
        val conn: URLConnection = url.openConnection()
        val rd = InputStreamReader(conn.getInputStream())
        val allpage = StringBuilder()
        val buffer = BufferedReader(rd)
        var line = buffer.readLine()
        while (line != null) {
            allpage.append(line)
            line = buffer.readLine()
        }
        out = allpage.toString()
        return out
    }
}
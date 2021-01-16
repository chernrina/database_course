package chernrina.flight_db.Activities

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import chernrina.flight_db.DownloadAsyncTask
import chernrina.flight_db.R
import chernrina.flight_db.sha512_5
import kotlinx.android.synthetic.main.registration.*

class RegistrationActivity: AppCompatActivity() {

    lateinit var prefs: SharedPreferences
    private lateinit var downloadAsyncTask: DownloadAsyncTask
    private val COMEIN = 1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.registration)
        prefs = getSharedPreferences(getString(R.string.loginField), Context.MODE_PRIVATE)
    }

    fun saveHuman(view: View) {
        val url_str = StringBuilder()
        url_str.append("http://192.168.0.4:8000/basic/getLogin/")
        url_str.append(login.text)
        url_str.append("/")
        downloadAsyncTask = DownloadAsyncTask()
        downloadAsyncTask.execute(url_str.toString())
        val res = downloadAsyncTask.get()
        if (res.isEmpty()) {
            downloadAsyncTask = DownloadAsyncTask()
            url_str.clear()
            url_str.append("http://192.168.0.4:8000/basic/saveHuman/")
            url_str.append(human_document.text)
            url_str.append("/")
            url_str.append(full_name.text)
            if (man.isChecked) url_str.append("/М/")
            else url_str.append("/Ж/")
            url_str.append(email.text)
            url_str.append("/")
            url_str.append(login.text)
            url_str.append("/")
            url_str.append(password.text.toString().sha512_5(login.text.toString()))
            url_str.append("/")
            downloadAsyncTask.execute(url_str.toString())
            val result = downloadAsyncTask.get()
            if (result == getString(R.string.successAdd)) {
                prefs.edit().putString(getString(R.string.currentLogin),login.text.toString()).apply()
                setResult(COMEIN)
                finish()
            } else Toast.makeText(this, result, Toast.LENGTH_LONG).show()
        } else Toast.makeText(this, getString(R.string.anotherLogin), Toast.LENGTH_LONG).show()
    }
}
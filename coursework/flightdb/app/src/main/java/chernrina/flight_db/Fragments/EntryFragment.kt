package chernrina.flight_db.Fragments

import android.app.AlertDialog
import android.app.Dialog
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.fragment.app.DialogFragment
import chernrina.flight_db.DownloadAsyncTask
import chernrina.flight_db.R
import chernrina.flight_db.sha512_5
import kotlinx.android.synthetic.main.entry_layout.view.*
import kotlinx.android.synthetic.main.entry_layout.view.login_entry

class EntryFragment(var login: StringBuilder) : DialogFragment()  {

    private lateinit var entryView : View

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val builder = AlertDialog.Builder(activity)
        entryView = LayoutInflater.from(context).inflate(R.layout.entry_layout, null)
        builder.setView(entryView)
        builder.setPositiveButton(getString(R.string.enrty)) { _, _ ->
            val url_str = StringBuilder()
            url_str.append("http://192.168.0.4:8000/basic/getPassword/")
            url_str.append(entryView.login_entry.text.toString())
            url_str.append("/")
            val downloadAsyncTask = DownloadAsyncTask()
            downloadAsyncTask.execute(url_str.toString())
            val result = downloadAsyncTask.get()
            if (entryView.password_entry.text.toString().sha512_5(entryView.login_entry.text.toString()) == result) {
                login.clear()
                login.append(entryView.login_entry.text.toString())
                Toast.makeText(
                    context,
                    "Здравствуйте, ${login.toString()}",
                    Toast.LENGTH_SHORT
                ).show()
                this.activity!!.setContentView(R.layout.activity_main_entry)
                dismiss()
            }
            else {
                Toast.makeText(context, getString(R.string.incorrectData), Toast.LENGTH_SHORT).show()
                dismiss()
            }
        }
        builder.setTitle(getString(R.string.logIn))
        return builder.create()
    }
}
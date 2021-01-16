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
import kotlinx.android.synthetic.main.change_info_fragment.view.*
import kotlinx.android.synthetic.main.change_info_fragment.view.name
import kotlinx.android.synthetic.main.lk_layout.*
import java.lang.StringBuilder


class ChangeInfoFragment : DialogFragment() {

    private lateinit var downloadAsyncTask: DownloadAsyncTask
    private lateinit var view_info : View

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val builder = AlertDialog.Builder(activity)
        view_info = LayoutInflater.from(context).inflate(R.layout.change_info_fragment, null)
        view_info.name.hint = activity!!.full_name.text
        view_info.gen.hint = activity!!.gender.text
        view_info.email.hint = activity!!.mail.text
        builder.setView(view_info)
        builder.setPositiveButton(getString(R.string.change)) { _, _ ->
            send()
        }
        builder.setNegativeButton(getString(R.string.cancel)) { _, _ ->
            dismiss()
        }
        builder.setTitle(getString(R.string.changeData))
        return builder.create()
    }

    private fun send() {
        downloadAsyncTask = DownloadAsyncTask()
        val url_str = StringBuilder()
        url_str.append("http://192.168.0.4:8000/basic/changeInfo/")
        url_str.append(activity!!.human_document.text)
        url_str.append('/')
        url_str.append(view_info.name.text)
        url_str.append('/')
        url_str.append(view_info.gen.text)
        url_str.append('/')
        url_str.append(view_info.email.text)
        url_str.append('/')
        downloadAsyncTask.execute(url_str.toString())
        val result = downloadAsyncTask.get()
        Toast.makeText(context, result, Toast.LENGTH_LONG).show()
        activity!!.full_name.text = view_info.name.text
        activity!!.gender.text = view_info.gen.text
        activity!!.mail.text = view_info.email.text
        dismiss()
    }

}
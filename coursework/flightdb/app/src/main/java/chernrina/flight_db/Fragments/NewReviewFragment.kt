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
import kotlinx.android.synthetic.main.new_review_layout.view.*
import java.lang.StringBuilder


class NewReviewFragment(private val name: String) : DialogFragment() {

    private lateinit var downloadAsyncTask: DownloadAsyncTask
    private lateinit var view_review : View

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val builder = AlertDialog.Builder(activity)
        view_review = LayoutInflater.from(context).inflate(R.layout.new_review_layout, null)
        builder.setView(view_review)
        builder.setPositiveButton(getString(R.string.send)) { _, _ ->
            send()
        }
        builder.setTitle(getString(R.string.newReview))
        return builder.create()
    }

    private fun send() {
        downloadAsyncTask = DownloadAsyncTask()
        val url_str = StringBuilder()
        url_str.append("http://192.168.0.4:8000/basic/saveReview/")
        url_str.append(name)
        url_str.append('/')
        url_str.append(view_review.airline.text)
        url_str.append('/')
        url_str.append(view_review.mark.text)
        url_str.append('/')
        downloadAsyncTask.execute(url_str.toString())
        val result = downloadAsyncTask.get()
        Toast.makeText(context, result, Toast.LENGTH_LONG).show()
        dismiss()
    }

}
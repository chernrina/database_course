package chernrina.flight_db.Fragments

import android.app.AlertDialog
import android.app.Dialog
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import androidx.annotation.RequiresApi
import androidx.fragment.app.DialogFragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import chernrina.flight_db.Adapters.AdapterAirlines
import chernrina.flight_db.DownloadAsyncTask
import chernrina.flight_db.R
import kotlinx.android.synthetic.main.airlines_layout.view.*

class AirlinesFragment: DialogFragment() {

    private lateinit var downloadAsyncTask: DownloadAsyncTask

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val url_str = "http://192.168.0.4:8000/basic/getTopAirlines/"
        downloadAsyncTask = DownloadAsyncTask()
        downloadAsyncTask.execute(url_str)
        val result = downloadAsyncTask.get()
        val builder = AlertDialog.Builder(activity)
        val airlinesView = LayoutInflater.from(context).inflate(R.layout.airlines_layout, null)
        builder.setView(airlinesView)

        val adapterAirlines =
            AdapterAirlines(result)
        val viewManager = LinearLayoutManager(context)
        downloadAsyncTask.cancel(true)

        airlinesView.airlines_list.apply {
            setHasFixedSize(true)
            layoutManager = viewManager as RecyclerView.LayoutManager?
            adapter = adapterAirlines
        }
        builder.setPositiveButton(getString(R.string.ok)) { _, _ ->
                dismiss()
        }
        builder.setTitle(getString(R.string.topAirlines))
        return builder.create()
    }
}
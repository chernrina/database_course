package chernrina.flight_db.Activities

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import chernrina.flight_db.Adapters.AdapterFlights
import chernrina.flight_db.DownloadAsyncTask
import chernrina.flight_db.R
import kotlinx.android.synthetic.main.flight_item.*
import kotlinx.android.synthetic.main.flights_layout.*

class FlightsActivity: AppCompatActivity() {

    private lateinit var downloadAsyncTask: DownloadAsyncTask
    private lateinit var adapterFlights: AdapterFlights
    private lateinit var viewManager: LinearLayoutManager
    private lateinit var login: String
    lateinit var prefs: SharedPreferences

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.flights_layout)
        login = intent.getStringExtra(getString(R.string.currentLogin))
        prefs = getSharedPreferences(getString(R.string.loginField), Context.MODE_PRIVATE)
        viewManager = LinearLayoutManager(this)
    }


    fun toSearch(view: View) {
        downloadAsyncTask = DownloadAsyncTask()
        val url_str = StringBuilder()
        url_str.append("http://192.168.0.4:8000/basic/getFlights/")
        url_str.append(city_from_text.text)
        url_str.append("/")
        url_str.append(city_to_text.text)
        url_str.append("/")
        url_str.append(date_from_text.text)
        url_str.append("/")
        downloadAsyncTask.execute(url_str.toString())
        loadRecycler()
    }

    fun loadRecycler() {
        val result = downloadAsyncTask.get()
        adapterFlights = if (result == getString(R.string.noSuchFlights) || result == getString(R.string.noSuchCity)) {
            Toast.makeText(this, result, Toast.LENGTH_SHORT).show()
            AdapterFlights("")
        } else {
            AdapterFlights(result)
        }
        downloadAsyncTask.cancel(true)
        flights_recycler_view.apply {
            setHasFixedSize(true)
            layoutManager = viewManager as RecyclerView.LayoutManager?
            adapter = adapterFlights
        }
    }

    fun onClickItem(view: View) {
        val builder = AlertDialog.Builder(this)
        builder.setMessage(getString(R.string.buyTicket))
        builder.setPositiveButton(getString(R.string.yes)) { _, _ ->
            if (!login.isEmpty()) {
                downloadAsyncTask = DownloadAsyncTask()
                val url_str = StringBuilder()
                url_str.append("http://192.168.0.4:8000/basic/saveTicket/")
                url_str.append(login)
                url_str.append("/")
                url_str.append(id_flight.text)
                url_str.append("/")
                downloadAsyncTask.execute(url_str.toString())
                val result = downloadAsyncTask.get()
                Toast.makeText(this, result, Toast.LENGTH_SHORT).show()
            } else Toast.makeText(this, getString(R.string.logIn), Toast.LENGTH_SHORT).show()
            finish()
        }

        builder.setNegativeButton(getString(R.string.no), null)
        val dialog = builder.create()
        dialog.show()
    }
}
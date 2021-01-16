package chernrina.flight_db.Activities

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import chernrina.flight_db.Adapters.AdapterTickets
import chernrina.flight_db.DownloadAsyncTask
import chernrina.flight_db.Fragments.ChangeInfoFragment
import chernrina.flight_db.Fragments.NewReviewFragment
import chernrina.flight_db.R
import kotlinx.android.synthetic.main.lk_layout.*

class LkActivity: AppCompatActivity() {

    lateinit var prefs: SharedPreferences
    private lateinit var downloadAsyncTask: DownloadAsyncTask
    private var url_str = StringBuilder()
    var login = StringBuilder()
    private lateinit var adapterTickets: AdapterTickets
    private lateinit var viewManager: LinearLayoutManager


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        login.append(intent.extras!!.get(getString(R.string.currentLogin)))
        prefs = getSharedPreferences(getString(R.string.loginField), Context.MODE_PRIVATE)
        setContentView(R.layout.lk_layout)
        viewManager = LinearLayoutManager(this)
    }

    override fun onStart() {
        super.onStart()
        downloadAsyncTask = DownloadAsyncTask()
        url_str.clear()
        url_str.append("http://192.168.0.4:8000/basic/getHuman/")
        url_str.append(login.toString())
        url_str.append('/')
        downloadAsyncTask.execute(url_str.toString())
        getResults()
    }

    private fun getResults() {
        val result = downloadAsyncTask.get()
        val elements = result.split('/')
        human_document.text = elements[0]
        full_name.text = elements[1]
        gender.text = elements[2]
        mail.text = elements[3]
        downloadAsyncTask.cancel(true)
    }

    fun onClick(view: View) {
        when(view.id) {
            newReview.id -> {
                val dialog =
                    NewReviewFragment(full_name.text.toString())
                dialog.show(supportFragmentManager, getString(R.string.tagReview))
            }
            mytickets.id -> {
                downloadAsyncTask = DownloadAsyncTask()
                url_str.clear()
                url_str.append("http://192.168.0.4:8000/basic/getTickets/")
                url_str.append(human_document.text)
                url_str.append('/')
                downloadAsyncTask.execute(url_str.toString())
                val result = downloadAsyncTask.get()
                if (result == getString(R.string.noTickets)) Toast.makeText(this, result, Toast.LENGTH_SHORT).show()
                else {
                    loadRecycler(result)
                }
                downloadAsyncTask.cancel(true)
            }
            change.id -> {
                val dialog = ChangeInfoFragment()
                dialog.show(supportFragmentManager, getString(R.string.tagChange))
            }
        }
    }

    private fun loadRecycler(result: String) {
        adapterTickets = AdapterTickets(result)

        tickets_list.apply {
            setHasFixedSize(false)
            layoutManager = viewManager as RecyclerView.LayoutManager?
            adapter = adapterTickets
        }
    }
}
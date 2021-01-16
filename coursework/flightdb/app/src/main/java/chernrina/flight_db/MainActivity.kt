package chernrina.flight_db

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import chernrina.flight_db.Activities.FlightsActivity
import chernrina.flight_db.Activities.LkActivity
import chernrina.flight_db.Activities.RegistrationActivity
import chernrina.flight_db.Fragments.AirlinesFragment
import chernrina.flight_db.Fragments.EntryFragment


class MainActivity : AppCompatActivity() {

    lateinit var prefs: SharedPreferences
    lateinit var entryView: View
    private val login = StringBuilder()
    private val REGISTRATION = 0
    private val COMEIN = 1

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        prefs = getSharedPreferences(getString(R.string.loginField), Context.MODE_PRIVATE)
        entryView = LayoutInflater.from(this).inflate(R.layout.entry_layout, null)
    }

    fun onClick(view: View) {
        when(view.id) {
            R.id.registry -> startActivityForResult(Intent(this, RegistrationActivity::class.java),REGISTRATION)
            R.id.toTopAirlines -> {
                val dialog = AirlinesFragment()
                dialog.show(supportFragmentManager, getString(R.string.airlines))
            }
            R.id.entry -> {
                val dialog = EntryFragment(login)
                dialog.show(supportFragmentManager, getString(R.string.autorization))
            }
            R.id.newTicket -> startActivity(Intent(this, FlightsActivity::class.java).putExtra(getString(
                            R.string.currentLogin),login.toString()))
            R.id.toPerson -> startActivity(Intent(this, LkActivity::class.java).putExtra(getString(
                R.string.currentLogin),login.toString()))
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when(resultCode) {
            COMEIN -> {
                setContentView(R.layout.activity_main_entry)
                login.append(prefs.getString(getString(R.string.currentLogin),"").toString())
            }
        }
    }
}

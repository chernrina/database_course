package chernrina.flight_db.Adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import chernrina.flight_db.R

class AdapterFlights(private val list_results: String) : RecyclerView.Adapter<AdapterFlights.MyViewHolder>() {

    inner class MyViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private var id_flight = view.findViewById<TextView>(R.id.id_flight)
        private var voyage = view.findViewById<TextView>(R.id.voyage)
        private var date_from = view.findViewById<TextView>(R.id.date_from)
        private var date_to = view.findViewById<TextView>(R.id.date_to)
        private var airplane = view.findViewById<TextView>(R.id.airplane)
        fun getFlight(): TextView {
            return id_flight
        }
        fun getVoyage(): TextView {
            return voyage
        }
        fun getDateFrom(): TextView {
            return date_from
        }
        fun getDateTo(): TextView {
            return date_to
        }
        fun getAirplane(): TextView {
            return airplane
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        val view  = LayoutInflater.from(parent.context).inflate(R.layout.flight_item,parent, false)
        return MyViewHolder(view)
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        val str = list_results.split("<br>")[position]
        val seq = str.split(' ')
        holder.getFlight().text = seq[0]
        holder.getVoyage().text = seq[1]
        holder.getDateFrom().text = (seq[2] + ' ' + seq[3])
        holder.getDateTo().text = (seq[4] + ' ' + seq[5])
        holder.getAirplane().text = seq[6]
    }

    override fun getItemCount(): Int {
        return list_results.split("<br>").size-1
    }
}
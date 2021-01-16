package chernrina.flight_db.Adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import chernrina.flight_db.R

class AdapterAirlines(private val list_results: String) : RecyclerView.Adapter<AdapterAirlines.MyViewHolder>() {
    inner class MyViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private var id_airline = view.findViewById<TextView>(R.id.id_airline)
        private var mark_sum = view.findViewById<TextView>(R.id.mark_sum)
        fun getAirline(): TextView {
            return id_airline
        }
        fun getMark(): TextView {
            return mark_sum
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        val view  = LayoutInflater.from(parent.context).inflate(R.layout.airline_item,parent, false)
        return MyViewHolder(view)
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        val str = list_results.split("<br>")[position]
        val seq = str.split('/')
        holder.getAirline().text = seq[0]
        holder.getMark().text = seq[1]
    }

    override fun getItemCount(): Int {
        return list_results.split("<br>").size-1
    }
}
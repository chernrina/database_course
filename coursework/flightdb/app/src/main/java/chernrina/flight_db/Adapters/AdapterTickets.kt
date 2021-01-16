package chernrina.flight_db.Adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import chernrina.flight_db.R

class AdapterTickets(private val list_results: String) : RecyclerView.Adapter<AdapterTickets.MyViewHolder>() {

    private val flight = "Flight "
    private val place = "Place "
    private val price = "Цена "

    inner class MyViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private var id_flight = view.findViewById<TextView>(R.id.flight_id)
        private var human_document = view.findViewById<TextView>(R.id.human_document)
        private var place = view.findViewById<TextView>(R.id.place)
        private var cost = view.findViewById<TextView>(R.id.cost)
        private var status = view.findViewById<TextView>(R.id.status)
        private var seq_num = view.findViewById<TextView>(R.id.seq_num)
        fun getFlight(): TextView {
            return id_flight
        }
        fun getDocum(): TextView {
            return human_document
        }
        fun getPlace(): TextView {
            return place
        }
        fun getCost(): TextView {
            return cost
        }
        fun getStatus(): TextView {
            return status
        }
        fun getSeq(): TextView {
            return seq_num
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        val view  = LayoutInflater.from(parent.context).inflate(R.layout.ticket_item,parent, false)
        return MyViewHolder(view)
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        val str = list_results.split("<br>")[position]
        val seq = str.split('/')
        holder.getDocum().text = seq[0]
        holder.getFlight().text = (flight + seq[1])
        holder.getPlace().text = (place + seq[2])
        holder.getStatus().text = seq[3]
        holder.getCost().text = (price + seq[4])
        holder.getSeq().text = seq[5]
    }

    override fun getItemCount(): Int {
        return list_results.split("<br>").size-1
    }
}
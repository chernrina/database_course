import random
import psycopg2
from datetime import date
import const
import time
import matplotlib.pyplot as plt
import threading

connection=psycopg2.connect(dbname='flight_db', user='user_flight', password='user', host='127.0.0.1')
cursor=connection.cursor()
connection.autocommit = True

cursor.execute("SELECT full_name FROM human")
names=cursor.fetchall()
cursor.execute("SELECT place FROM ticket")
places=cursor.fetchall()
cursor.execute("SELECT id_voyage FROM voyage")
voyages=cursor.fetchall()
cursor.execute("SELECT id_airline FROM airline")
airlines=cursor.fetchall()

query_1="SELECT human_document from human WHERE full_name = %(name)s;"
query_2="SELECT id_flight, voyage.airport_from AS airport_from, voyage.airport_to AS airport_to FROM flight"\
" INNER JOIN voyage ON voyage.id_voyage = %(voyage)s LIMIT 20;"
query_3="SELECT human_document,cost FROM ticket WHERE cost BETWEEN 10000 AND 25000 AND seq_num>2;"
query_4="INSERT INTO public.rate (baggage, select_seat, class) VALUES (%(baggage)s, %(select_seat)s, %(class)s);"
query_5="INSERT INTO public.order (quantity, customer) VALUES (5,%(customer)s);"
query_6="SELECT id_voyage, airline.mark_sum AS markOfAirline FROM voyage INNER JOIN airline ON airline.id_airline = %(airline)s"\
" WHERE id_voyage LIKE 'A%%'"
query_7="SELECT id_flight,voyage,airplane FROM flight WHERE voyage=%(voyage)s;"
query_8="SELECT id_ticket from ticket WHERE place = %(place)s AND trip_id<100;"
query_9="SELECT human_document, full_name FROM"\
" (SELECT human.human_document, full_name, extract(month from flight.date_from) as mon, count(*) as cnt"\
" FROM human INNER JOIN ticket on ticket.human_document = human.human_document"\
" INNER JOIN flight on flight.id_flight = ticket.flight"\
" WHERE flight.date_from >= (current_date - integer '365')"\
" GROUP BY human.human_document, full_name, extract(month from flight.date_from)"\
" HAVING count(*)>=2) as query"\
" GROUP BY human_document, full_name"\
" HAVING human_document LIKE %(docum)s"

query_list=(query_1,query_2,query_3,query_4,query_5,query_6,query_7,query_8)

curr_res_cosntant_threads=[[]]
curr_res_dinamic_threads=[]

before = True

def main():
	drop_index()
	check_explain_analyze()
	constant_threads(1)
	constant_threads(2)
	dinamic_threads(2000)
	optimize()
	#optimize_9()
	check_explain_analyze()
	constant_threads(1)	
	constant_threads(2)
	dinamic_threads(2000)	


def constant_threads(num_threads):
	curr_res_cosntant_threads.clear()
	for t in range(num_threads):
		dbt = DBThread_constant_threads(t)
		dbt.start()
	while threading.activeCount() > 1:
		time.sleep(1)
	plot_x=[k for k in range(401,10000,200)]
	plot_y=[]
	for i in range(len(curr_res_cosntant_threads[0])):
		curr_sum=0
		for j in range(num_threads):
			curr_sum+=curr_res_cosntant_threads[j][i]
		plot_y.append(curr_sum/num_threads)
	plt.plot(plot_x,plot_y,linewidth=2.0)
	plt.xlabel('Запросов в секунду')
	plt.ylabel('Время ответа на один запрос, мс')
	if before:
		plt.title("Before. Num threads: {}".format(num_threads))
	else:
		plt.title("After. Num threads: {}".format(num_threads))
	plt.show()

def dinamic_threads(num_querys):
	plot_x=[k for k in range(1,31)]
	plot_y=[]
	for num_threads in range(1,31):
		curr_res_dinamic_threads.clear()
		for t in range(num_threads):
			dbt = DBThread_dinamic_threads(num_querys)
			dbt.start()

		while threading.activeCount() > 1:
			time.sleep(1)

		plot_y.append(sum(curr_res_dinamic_threads)/len(curr_res_dinamic_threads))


	plt.plot(plot_x,plot_y,linewidth=2.0)
	plt.xlabel('Количество потоков')
	plt.ylabel('Время ответа на один запрос, мс')
	if before:
		plt.title("Before. Dinamic thread num")
	else:
		plt.title("After. Dinamic thread num")
	plt.show()

def drop_index():
	cursor.execute("DROP INDEX IF EXISTS human_name")
	cursor.execute("DROP INDEX IF EXISTS ticket_place")
	cursor.execute("DROP INDEX IF EXISTS voyage_id_voyage")
	cursor.execute("DROP INDEX IF EXISTS flight_voyage")
	cursor.execute("DROP INDEX IF EXISTS airline_id_airline")

	cursor.execute("DROP INDEX IF EXISTS human_document")
	cursor.execute("DROP INDEX IF EXISTS flight_date")

	cursor.execute("DROP INDEX IF EXISTS hd")
	cursor.execute("DROP INDEX IF EXISTS hf")
	cursor.execute("DROP INDEX IF EXISTS td")
	cursor.execute("DROP INDEX IF EXISTS tf")
	cursor.execute("DROP INDEX IF EXISTS fi")
	cursor.execute("DROP INDEX IF EXISTS hum")


def optimize():
	cursor.execute("CREATE INDEX human_name ON human(full_name);")
	cursor.execute("CREATE INDEX ticket_place ON ticket(place) WHERE trip_id<100;")
	cursor.execute("CREATE INDEX voyage_id_voyage ON voyage(id_voyage)")
	cursor.execute("CREATE INDEX flight_voyage ON flight(voyage)")
	cursor.execute("CREATE INDEX airline_id_airline ON airline(id_airline)")

	cursor.execute("CREATE INDEX human_document ON human(human_document)")

	global before
	before = False

def optimize_9():
	
	cursor.execute("CREATE INDEX hd ON human(human_document)")
	cursor.execute("CREATE INDEX hf ON human(full_name)")
	cursor.execute("CREATE INDEX td ON ticket(human_document)")
	cursor.execute("CREATE INDEX tf ON ticket(flight)")
	cursor.execute("CREATE INDEX fi ON flight(id_flight)")
	cursor.execute("CREATE INDEX hum ON human(human_document, full_name)")

	global before
	before = False

def exec_query_before(query,thread_cursor):
	if query==query_1:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_1, {"name":random.choice(names)})
	elif query == query_2:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_2, {"voyage":random.choice(voyages)})
	elif query == query_3:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_3)
	elif query == query_4:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_4, {"baggage":random.choice(const.baggage),
			"select_seat":random.choice(const.select_seat),"class":random.choice(const.classes)})
	elif query == query_5:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_5, {"customer":random.choice(names)})
	elif query == query_6:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_6, {"airline":random.choice(airlines)}) 
	elif query == query_7:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_7, { "voyage": random.choice(voyages)})
	elif query == query_8:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_8, {"place":random.choice(places)})
	elif query == query_9:
		thread_cursor.execute("EXPLAIN ANALYZE " + query_9, {"docum": (str(random.randint(1,9)) + "%%")})
	else:
		print("Wrong query!")
	fetch_res=thread_cursor.fetchall()
	try:
		return float(fetch_res[-1][0].split(" ")[2])+float(fetch_res[-2][0].split(" ")[2])
	except ValueError:
		return float(fetch_res[-1][0].split(" ")[2])+float(fetch_res[-2][0].split(" ")[4].split("=")[1])+float(fetch_res[-3][0].split(" ")[2])


def exec_query_after(query,thread_cursor):
	if query==query_1:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query1 (%s);", random.choice(names))
	elif query == query_2:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query2 (%s);", random.choice(voyages))
	elif query == query_3:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query3;")
	elif query == query_4:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query4 (%s,%s,%s);", (random.choice(const.baggage),
			random.choice(const.select_seat), random.choice(const.classes)))
	elif query == query_5:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query5 (%s);", random.choice(names))
	elif query == query_6:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query6 (%s);", random.choice(airlines))
	elif query == query_7:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query7 (%s);", random.choice(voyages))
	elif query == query_8:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query8 (%s);", random.choice(places))
	elif query == query_9:
		thread_cursor.execute("EXPLAIN ANALYZE EXECUTE query9 (%(docum)s);", {"docum": (str(random.randint(1,9)) + "%%")})
	else:
		print("Wrong query!")
	fetch_res=thread_cursor.fetchall()
	try:
		return float(fetch_res[-1][0].split(" ")[2])+float(fetch_res[-2][0].split(" ")[2])
	except ValueError:
		return float(fetch_res[-1][0].split(" ")[2])+float(fetch_res[-2][0].split(" ")[4].split("=")[1])+float(fetch_res[-3][0].split(" ")[2])		

def check_explain_analyze():
	cursor.execute("EXPLAIN ANALYZE " + query_9, {"docum": (str(random.randint(1,9)) + "%%")})
	print(cursor.fetchall())
	print("\n")

class DBThread_constant_threads(threading.Thread):
	def __init__(self,curr_thread):

		self.curr_thread=curr_thread
		threading.Thread.__init__(self)
		self.conn = psycopg2.connect(dbname='flight_db', user='user_flight', password='user', host='127.0.0.1')
		self.cur = self.conn.cursor()

		global before

		if not before:
			self.cur.execute("PREPARE query1 (varchar(100)) AS SELECT human_document from human WHERE full_name = $1;")
			self.cur.execute("PREPARE query2 (varchar(10)) AS SELECT id_flight, voyage.airport_from AS airport_from, voyage.airport_to AS airport_to FROM flight"\
" INNER JOIN voyage ON voyage.id_voyage = $1 LIMIT 20;")
			self.cur.execute("PREPARE query3 AS SELECT human_document,cost FROM ticket WHERE cost BETWEEN 10000 AND 20000 AND seq_num>2;")
			self.cur.execute("PREPARE query4 (varchar(50),varchar(20),varchar(30)) AS INSERT INTO public.rate (baggage, select_seat, class) VALUES ($1,$2,$3);")
			self.cur.execute("PREPARE query5 (varchar(100)) AS INSERT INTO public.order (quantity, customer) VALUES (5,$1);")
			self.cur.execute("PREPARE query6 (varchar(30)) AS SELECT id_voyage, airline.mark_sum AS markOfAirline FROM voyage INNER JOIN airline ON airline.id_airline = $1"\
" WHERE id_voyage LIKE 'A%%';")
			self.cur.execute("PREPARE query7 (varchar(10)) AS SELECT id_flight,voyage,airplane FROM flight WHERE voyage= $1;")
			self.cur.execute("PREPARE query8 (varchar(5)) AS SELECT id_ticket from ticket WHERE place = $1 AND trip_id<100;")
			self.cur.execute("PREPARE query9 (varchar) AS SELECT human_document, full_name FROM"\
" (SELECT human.human_document, full_name, extract(month from flight.date_from) as mon, count(*) as cnt"\
" FROM human INNER JOIN ticket on ticket.human_document = human.human_document"\
" INNER JOIN flight on flight.id_flight = ticket.flight"\
" WHERE flight.date_from >= (current_date - integer '365')"\
" GROUP BY human.human_document, full_name, extract(month from flight.date_from)"\
" HAVING count(*)>=2) as query"\
" GROUP BY human_document, full_name"\
" HAVING human_document LIKE $1 ;")

	def run(self):
		for i in range(401,10000,200):
			results=[]
			for j in range(0,i):
				print(j)
				random_query=random.choice(query_list)
				if before:
					results.append(exec_query_before(random_query,self.cur))
				else:
					results.append(exec_query_after(random_query,self.cur))
			if len(curr_res_cosntant_threads)<self.curr_thread+1:
				curr_res_cosntant_threads.append([])
			curr_res_cosntant_threads[self.curr_thread].append(sum(results)/len(results))
		self.conn.commit() 

class DBThread_dinamic_threads(threading.Thread):
	def __init__(self,num_querys):

		self.num_querys=num_querys
		threading.Thread.__init__(self)
		self.conn = psycopg2.connect(dbname='flight_db', user='user_flight', password='user', host='127.0.0.1')
		self.cur = self.conn.cursor()

		global before

		if not before:
			self.cur.execute("PREPARE query1 (varchar(100)) AS SELECT human_document from human WHERE full_name = $1;")
			self.cur.execute("PREPARE query2 (varchar(10)) AS SELECT id_flight, voyage.airport_from AS airport_from, voyage.airport_to AS airport_to FROM flight"\
" INNER JOIN voyage ON voyage.id_voyage = $1 LIMIT 20;")
			self.cur.execute("PREPARE query3 AS SELECT human_document,cost FROM ticket WHERE cost BETWEEN 10000 AND 20000 AND seq_num>2;")
			self.cur.execute("PREPARE query4 (varchar(50),varchar(20),varchar(30)) AS INSERT INTO public.rate (baggage, select_seat, class) VALUES ($1,$2,$3);")
			self.cur.execute("PREPARE query5 (varchar(100)) AS INSERT INTO public.order (quantity, customer) VALUES (5,$1);")
			self.cur.execute("PREPARE query6 (varchar(30)) AS SELECT id_voyage, airline.mark_sum AS markOfAirline FROM voyage INNER JOIN airline ON airline.id_airline = $1"\
" WHERE id_voyage LIKE 'A%%';")
			self.cur.execute("PREPARE query7 (varchar(10)) AS SELECT id_flight,voyage,airplane FROM flight WHERE voyage= $1;")
			self.cur.execute("PREPARE query8 (varchar(5)) AS SELECT id_ticket from ticket WHERE place = $1 AND trip_id<100;")
			self.cur.execute("PREPARE query9 (varchar) AS SELECT human_document, full_name FROM"\
" (SELECT human.human_document, full_name, extract(month from flight.date_from) as mon, count(*) as cnt"\
" FROM human INNER JOIN ticket on ticket.human_document = human.human_document"\
" INNER JOIN flight on flight.id_flight = ticket.flight"\
" WHERE flight.date_from >= (current_date - integer '365')"\
" GROUP BY human.human_document, full_name, extract(month from flight.date_from)"\
" HAVING count(*)>=2) as query"\
" GROUP BY human_document, full_name"\
" HAVING human_document LIKE $1;")

	def run(self):
		results=[]
		for j in range(0,self.num_querys+1):
			print(j)
			random_query=random.choice(query_list)
			if before:
				results.append(exec_query_before(random_query,self.cur))
			else:
				results.append(exec_query_after(random_query,self.cur))
		curr_res_dinamic_threads.append(sum(results)/len(results))
		self.conn.commit() 

if __name__ == "__main__":
	main()

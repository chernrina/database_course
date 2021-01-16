import random
import psycopg2
from datetime import date, timedelta
import const
import argparse
import sys
import math
from statistics import *

connection = psycopg2.connect(dbname='flight_db', user='user_flight', password='user', host='127.0.0.1')
cursor = connection.cursor()

names_man = const.names_man
names_woman = const.names_woman
letters = const.letters
emails = const.emails
classes = const.classes
baggage = const.baggage
select_seat = const.select_seat
cities = const.cities
airplanes = const.airplanes
airlines = const.airlines
airports = const.airports
human_doc = []
airports_all = []
voyages = []

def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--human', nargs = '+', type = str)
	parser.add_argument('-r', '--review', nargs = '+', type = str)
	parser.add_argument('-v', '--voyage', nargs = '+', type = str)
	parser.add_argument('-o', '--order', nargs = '+', type = str)
	parser.add_argument('-t', '--timetable', nargs = '+', type = str)
	return parser

def main():

	parser = createParser()
	args = parser.parse_args(sys.argv[1:])

	if (len(sys.argv) == 1):

		cursor.execute('DELETE FROM ticket')
		cursor.execute('ALTER SEQUENCE id_ticket_seq RESTART')

		cursor.execute('DELETE FROM trip')
		cursor.execute('ALTER SEQUENCE id_trip_seq RESTART')

		cursor.execute('DELETE FROM public.order')
		cursor.execute('ALTER SEQUENCE id_order_seq RESTART')

		cursor.execute('DELETE FROM human')

		cursor.execute('DELETE FROM rate')
		cursor.execute('ALTER SEQUENCE id_rate_seq RESTART')

		cursor.execute('DELETE FROM review')
		cursor.execute('ALTER SEQUENCE id_review_seq RESTART')

		cursor.execute('DELETE FROM timetable')
		cursor.execute('ALTER SEQUENCE id_timetable_seq RESTART')

		cursor.execute('DELETE FROM flight')
		cursor.execute('ALTER SEQUENCE id_flight_seq RESTART')

		cursor.execute('DELETE FROM voyage')

		cursor.execute('DELETE FROM airline')		

		cursor.execute('DELETE FROM airplane')

		cursor.execute('DELETE FROM airport')

		human_generation(100)

		rate_generation()

		airline_generation()

		airplane_generation()

		airport_generation()

		connection.commit()

		voyage_generation(100)

		review_generation(50)		

		connection.commit()

		timetable_generation(20)

		order_generation(50)

	else:

		if args.human:
			if(len(args.human) > 5):
				print("More than 5 arguments after human")
				sys.exit(1)
			else:
				human_generation(args.human[0], *args.human[1:])

		if args.review:
			if(len(args.review) > 3):
				print("More than 3 arguments after review")
				sys.exit(1)
			else:
				review_generation(args.review[0], *args.review[1:])

		if args.voyage:
			if(len(args.voyage) > 3):
				print("More than 3 arguments after voyage")
				sys.exit(1)
			else:
				voyage_generation(args.voyage[0], *args.voyage[1:])

		if args.order:
			if(len(args.order) > 6):
				print("More than 6 arguments after order")
				sys.exit(1)
			else:
				order_generation(args.order[0], *args.order[1:])

		if args.timetable:
			if(len(args.timetable) > 1):
				print("More than 1 arguments after order")
				sys.exit(1)
			else:
				timetable_generation(args.timetable[0])

	connection.commit()
	connection.close()

def human_generation(amount=0, surname=0, name=0, fathers_name=0, gender=0):

	flag = surname != 0 and name != 0 and fathers_name != 0 and gender != 0

	cursor.execute('SELECT human_document FROM public.human')
	human_doc_all = cursor.fetchall()

	for i in range(len(human_doc_all)):
		human_doc.append(human_doc_all[i][0])

	human = ''

	for count in range(int(amount)):

		newDoc = str(random.randrange(1000,10000,1)) + ' ' + str(random.randrange(100000,1000000,1))
		while (newDoc in human_doc):
			doc = str(random.randrange(1000,10000,1)) + ' ' + str(random,randrange(100000,1000000,1))

		human_doc.append(newDoc)

		newEmail = ''
		for j in range(random.randrange(1,15,1)):
			newEmail = newEmail+random.choice(letters)
		newEmail = newEmail+random.choice(emails)

		if (flag):
			human = human + '( \'' + str(newDoc) + '\', \'' + surname + ' ' + name + ' ' + fathers_name + '\', \'' + gender + '\',\'' + newEmail + '\'),'
			print('Successful adding')
		else:
			if (random.randrange(0,2,1)):
				human = human + '( \'' + str(newDoc) + '\', \'' + random.choice(names_man) + '\', \'' + 'M' + '\',\'' + newEmail + '\'),'
				
			else: 
				human = human + '( \'' + str(newDoc) + '\', \'' + random.choice(names_woman) + '\', \'' + 'Ж' + '\',\'' + newEmail + '\'),'

	exec_str = 'INSERT INTO public.human (human_document, full_name, gender, email) VALUES {}'.format(human)
	cursor.execute(exec_str[:len(exec_str)-1])

def rate_generation():

	rate = ''

	for i in range(len(classes)):
		for j in range(len(baggage)):
			for k in range(len(select_seat)):
				rate = rate + '( \'' + baggage[j] + '\', \'' + select_seat[k] + '\', \'' + classes[i] +'\'),'

	exec_str = 'INSERT INTO public.rate (baggage, select_seat, class) VALUES {}'.format(rate)
	cursor.execute(exec_str[:len(exec_str)-1])

def airline_generation():

	airline = ''

	for i in range(len(airlines)):
		element = airlines[i].split(' \ ')
		airline = airline + '( \'' + element[0] + '\',\'' + element[1] + '\',\'' + element[2] + '\',\'' + str(0) + '\'),'

	exec_str = 'INSERT INTO public.airline (id_airline, supervisor, create_in, mark_sum) VALUES {}'.format(airline)
	cursor.execute(exec_str[:len(exec_str)-1])

def review_generation(amount, airline=0, mark=0):

	flag = airline != 0 and mark != 0

	review = ''

	for count in range(int(amount)):
		if (flag):
			review = review + '( \'' + random.choice(names_man) + '\',\'' + airline + '\',\'' + mark + '\'),'
			print('Successful adding') 
			
		else:
			review = review + '( \'' + random.choice(names_man) + '\',\'' + random.choice(airlines).split(' \ ')[0] + '\',\'' + str(random.randrange(0,10,1)) + '\'),'

	exec_str = 'INSERT INTO public.review (human_name, airline, mark) VALUES {}'.format(review)
	cursor.execute(exec_str[:len(exec_str)-1])

	connection.commit()

	for i in range(len(airlines)):

		elem = airlines[i].split(' \ ')[0]

		cursor.execute("""SELECT mark FROM public.review WHERE airline=%s""",(elem,))
		results = cursor.fetchall()	

		if(len(results)!=0):
			sums = 0	
			for j in range(len(results)):
				sums = sums + results[j][0]
			sums = sums / len(results)
			cursor.execute('UPDATE airline SET mark_sum=%s WHERE id_airline=%s', (sums,elem,))

def airplane_generation():
	
	airplane = ''
	for i in range(len(airplanes)):
		element = airplanes[i].split(' \ ')
		airplane = airplane + '( \'' + element[0] + '\',\'' + element[1] + '\'),'

	exec_str = 'INSERT INTO public.airplane (id_airplane, places) VALUES {}'.format(airplane)
	cursor.execute(exec_str[:len(exec_str)-1])

def airport_generation():

	airport = ''
	for i in range(len(airports)):
		element = airports[i].split('|')
		airport = airport + '( \'' + element[0] + '\',\'' + element[2] + '\',\'' + element[1] + '\'),'

	exec_str = 'INSERT INTO public.airport (id_airport, city, full_name) VALUES {}'.format(airport)
	cursor.execute(exec_str[:len(exec_str)-1])

def voyage_generation(amount, airp_from=0, airp_to=0,intro=0):

	flag = airp_from != 0 and airp_to != 0

	cursor.execute('SELECT id_voyage FROM public.voyage')
	voyages_all = cursor.fetchall()
	for i in range(len(voyages_all)):
		voyages.append(voyages_all[i][0])

	for count in range(int(amount)):

		elem = random.choice(letters) + str(random.randrange(0,100,1)) + random.choice(letters) + str(random.randrange(0,10,1))
		while (elem in voyages):
			elem = random.choice(letters) + str(random.randrange(0,100,1)) + random.choice(letters) + str(random.randrange(0,10,1))
		voyages.append(elem)

		if (flag):
			if (airp_from == airp_to):
				print("Two airports are the same")
				sys.exit(1)
			cursor.execute('INSERT INTO public.voyage (id_voyage, airport_from, airport_to, airline) VALUES (%s,%s,%s,%s)', 
				(elem,airp_from,airp_to,airlines[random.randrange(1,len(airlines),1)].split(' \ ')[0]))
			flight_generation(elem)
			if (intro != 0): return elem
			else: print('Successful adding')

		else:
			airport_from = airports[random.randint(0,cities-1)].split('|')[0]
			airport_to = airports[random.randint(0,cities-1)].split('|')[0]
			while (airport_to == airport_from):
				airport_to = airports[random.randrange(1,cities,1)].split('|')[0]
			cursor.execute('INSERT INTO public.voyage (id_voyage, airport_from, airport_to, airline) VALUES (%s,%s,%s,%s)', 
				(elem,airport_from,airport_to,airlines[random.randrange(1,len(airlines),1)].split(' \ ')[0]))
			flight_generation(elem)


def flight_generation(voyage):

	flight = ''
	for i in range(const.month):
		random_date = date.today() + timedelta(days=i,seconds=random.randint(0,3600))
		hour_from = random.randint(0,23)
		hour_to = random.randint(0,23)
		if (hour_to < hour_from or hour_from == 0): 
			random_date_to = random_date + timedelta(days=1)
		else: random_date_to = random_date
		date_time_from = " " + str(hour_from) + ":" + str(random.randint(0,59)) + ":00"
		date_time_to = " " + str(hour_to) + ":" + str(random.randint(0,59)) + ":00"
		flight = flight + '( \'' + voyage + '\',\'' + str(random_date) + date_time_from + '\',\'' + str(random_date_to) + date_time_to + '\',\'' + airplanes[random.randrange(1,len(airplanes),1)].split(' \ ')[0] + '\'),'

	exec_str = 'INSERT INTO public.flight (voyage, date_from, date_to, airplane) VALUES {}'.format(flight)
	cursor.execute(exec_str[:len(exec_str)-1])	

def timetable_generation(amount):

	cursor.execute('SELECT count(id_timetable) FROM public.timetable')
	last_date = cursor.fetchone()
	cursor.execute('SELECT date_timetable FROM public.timetable WHERE id_timetable=%s',(last_date,))
	last_date = cursor.fetchone()
	if (last_date is not None):
		last_date = last_date[0] + timedelta(days=1)
	else:
		last_date = date.today()

	timetable = ''
	for count in range(int(amount)):
		date_timetable = last_date + timedelta(days=count)
		date_flight = str(date_timetable) + " 23:59:59"
		cursor.execute("""SELECT id_flight,voyage FROM public.flight WHERE date_from < %s """,(date_flight,))
		results = cursor.fetchall()
		for i in range(len(results)):
			timetable = timetable + '( \'' + str(date_timetable) + '\',\'' + str(results[i][1]) + '\',\'' + str(results[i][0]) + '\'),'

	exec_str = 'INSERT INTO public.timetable (date_timetable, voyage, flight) VALUES {}'.format(timetable)
	cursor.execute(exec_str[:len(exec_str)-1])

def order_generation(amount,quantity=0,name=0,city_from=0,city_to=0,transit=0):
	flag = quantity != 0 and name != 0

	for count in range(len(airports)):
		airports_all.append(airports[count].split('|')[0])

	for count in range(int(amount)):
		if (not flag):
			if (random.randrange(0,2,1)): name = random.choice(names_woman)
			else: name = random.choice(names_man)
			quantity = random.randint(1,3)
		cursor.execute('INSERT INTO public.order (quantity, customer) VALUES (%s,%s)', 
			(quantity, name))
		if (not flag): 
			if (random.randint(0,2)): transit = 1
		trip_generation(quantity,flag,city_from,city_to,transit)

def trip_generation(amount,flag,city_from=0,city_to=0,transit=0):
	flag = city_from != 0 and city_to != 0

	cursor.execute("SELECT count(id_order) FROM public.order")
	order_id = cursor.fetchone()[0]

	if (flag):
		cursor.execute('SELECT id_airport FROM public.airport WHERE city=%s',(city_from,))
		airport_from = cursor.fetchone()
		cursor.execute('SELECT id_airport FROM public.airport WHERE city=%s',(city_to,))
		airport_to = cursor.fetchone()
		if (airport_to is None or airport_from is None):
			print('Such city does not exists')
			sys.exit(1)
		cursor.execute('SELECT id_voyage FROM public.voyage WHERE airport_from=%s AND airport_to=%s LIMIT 10', (airport_from,airport_to))
		voyage_id = cursor.fetchone()
		if (voyage_id is None): voyage_id = voyage_generation(1,airport_from,airport_to,1)		

	else:
		cursor.execute('SELECT id_voyage FROM public.voyage LIMIT 50')
		voyages_all = cursor.fetchall()
		voyage_id = random.choice(voyages_all)[0]

	if (not flag):
		cursor.execute('SELECT airport_from FROM public.voyage WHERE id_voyage=%s',(voyage_id,))
		airport_from = cursor.fetchone()[0]
		cursor.execute('SELECT airport_to FROM public.voyage WHERE id_voyage=%s',(voyage_id,))
		airport_to = cursor.fetchone()[0]
		cursor.execute('SELECT city FROM public.airport WHERE id_airport=%s',(airport_from,))
		city_from = cursor.fetchone()[0]
		cursor.execute('SELECT city FROM public.airport WHERE id_airport=%s',(airport_to,))
		city_to = cursor.fetchone()[0]
	cursor.execute('INSERT INTO public.trip (order_id, city_from, city_to) VALUES (%s,%s,%s)',
		(order_id,city_from, city_to))
	if (transit!=0): flag = True
	else: flag = False
	ticket_generation(int(amount), voyage_id,flag, airport_from, airport_to)


def ticket_generation(amount,voyage_id, flag,transit_airport,airport_to):
	seat = const.seat
	status = const.status
	cursor.execute("SELECT id_flight FROM public.flight WHERE voyage=%s AND date_from>%s AND date_from<%s ORDER BY date_from ASC LIMIT 5",(voyage_id, date.today(), date.today() + timedelta(days=2)))
	flight_id = cursor.fetchone()[0]
	cursor.execute("SELECT count(id_rate) FROM public.rate")
	rate_amount = cursor.fetchone()[0]
	cursor.execute("SELECT count(id_trip) FROM public.trip")
	trip_id = str(cursor.fetchone()[0])
	cursor.execute('SELECT human_document FROM public.human')
	human_doc = cursor.fetchall()

	ticket=''
	if (flag and amount != 1):
		transit = random.randint(2,int(amount))
		amount = amount-transit

	for count in range(amount):
		place = str(random.randint(1,30)) + random.choice(seat)
		ticket = ticket + '( \'' + random.choice(human_doc)[0] + '\',\'' + str(flight_id) + '\',\'' + place + '\',\'' + random.choice(status) + '\',\'' + str(random.randrange(1,100000,50)) + '\',\'' + str(random.randint(1,rate_amount)) + '\',\'' + trip_id + '\',\'' + str(1) + '\'),'
	
	if (flag and amount != 1):
		document = random.choice(human_doc)[0]
		for count in range(transit):

			place = str(random.randint(1,30)) + random.choice(seat)
			if (count == transit-1):
				cursor.execute('SELECT id_voyage FROM public.voyage WHERE airport_from=%s AND airport_to=%s LIMIT 10',(transit_airport,airport_to,))
			else:
				cursor.execute('SELECT id_voyage FROM public.voyage WHERE airport_from=%s AND airport_to!=%s LIMIT 10',(transit_airport, airport_to,))

			listOfVoyages = cursor.fetchall()
			
			airport_for_voyage = random.choice(airports_all)
			while (airport_for_voyage == transit_airport or airport_for_voyage == airport_to):
				airport_for_voyage = random.choice(airports_all)
			if (count == transit-1): airport_for_voyage = airport_to

			if (len(listOfVoyages) < 2):
				new_voyage_id = voyage_generation(1,transit_airport,airport_for_voyage,1)				
			else:
				new_voyage_id = random.choice(listOfVoyages)[0]	
				while new_voyage_id == voyage_id:
					new_voyage_id = random.choice(listOfVoyages)[0]	
			
			if (count == 0):
				cursor.execute('SELECT id_flight FROM public.flight WHERE voyage=%s AND date_from>%s AND date_from<%s ORDER BY date_from ASC LIMIT 5',(new_voyage_id, date.today(), date.today() + timedelta(days=2)))
				flight_id = cursor.fetchone()[0] 
				cursor.execute('SELECT date_to FROM public.flight WHERE id_flight=%s',(flight_id,))
				date_from = cursor.fetchone()[0]
			else:
				date_check = date_from + timedelta(days=2)
				flight_id = None
				while (flight_id is None):
					cursor.execute('SELECT id_flight FROM public.flight WHERE voyage=%s AND date_from<%s AND date_from>%s LIMIT 5',(new_voyage_id, date_check,date_from))
					flight_id = cursor.fetchone()
					if (flight_id is None):
						flight_generation(new_voyage_id)
				flight_id = flight_id[0]
				cursor.execute('SELECT date_to FROM public.flight WHERE id_flight=%s',(flight_id,))
				date_from = cursor.fetchone()[0]

			transit_airport = airport_for_voyage
			ticket = ticket + '( \'' + document + '\',\'' + str(flight_id) + '\',\'' + place + '\',\'' + random.choice(status) + '\',\'' + str(random.randrange(1,100000,50)) + '\',\'' + str(random.randint(1,rate_amount)) + '\',\'' + trip_id + '\',\'' + str(count+1) + '\'),'
			print(trip_id) #!!! убрать

	exec_str = 'INSERT INTO public.ticket (human_document,flight, place, status, cost, rate, trip_id, seq_num) VALUES {}'.format(ticket)
	cursor.execute(exec_str[:len(exec_str)-1])

if __name__ == "__main__":
	main()	
from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
from tables import models
from django.db.models import F
import random


def getLogin(request,in_login):
	login = models.Human.objects.filter(login=in_login)
	export_list = ""
	if login.exists():
		export_list = "Such login already exists"
	return HttpResponse(export_list)

def getPassword(request,in_login):
	password = models.Human.objects.filter(login=in_login)
	export_list = ""
	if not password.exists():
		export_list = "No such login"
	else:
		export_list = password[0].password

	return HttpResponse(export_list)


def getHuman(request, in_login):
	human = models.Human.objects.filter(login=in_login)
	export_list = ""
	if not human.exists():
		export_list = "No such login"

	else: export_list = human[0].human_document + '/' + human[0].full_name + '/' + human[0].gender + '/' + human[0].email

	return HttpResponse(export_list)

def getFlights(request,city_from,city_to,date_f):
	export_list = ""
	airport_f = models.Airport.objects.filter(city=city_from)
	airport_t = models.Airport.objects.filter(city=city_to)

	if not airport_f.exists() or not airport_t.exists():
		export_list = "No such city"
		return HttpResponse(export_list)

	voyages = models.Voyage.objects.filter(airport_from=airport_f[0].id_airport, airport_to=airport_t[0].id_airport)
	
	if not voyages.exists():
		export_list = "No such flights"
	else:

		flights=models.Flight.objects.filter(voyage=voyages[0].id_voyage, date_from__gte=date_f).order_by('date_from') [:5]

		for i in list(voyages):
			if (i != voyages[0]):
				flights = models.Flight.objects.filter(voyage=i.id_voyage, date_from__gte=date_f).order_by('date_from') [:5]

			for j in range(len(list(flights))):
				export_list = export_list + str(flights[j].id_flight) + ' ' + str(flights[j].voyage.id_voyage) + ' ' + str(flights[j].date_from) + ' ' + str(flights[j].date_to) + ' ' + str(flights[j].airplane.id_airplane) + "<br>"

	return HttpResponse(export_list)

def saveHuman(request,doc,f_name,gen,mail,log,key):
	prevDoc = models.Human.objects.filter(human_document=doc)
	export_list=""
	if prevDoc.exists():
		export_list = "Such document already exists"
	else:
		newDoc = models.Human.objects.create(human_document=doc,full_name=f_name,gender=gen,email=mail,login=log,password=key)
		newDoc.save()
		export_list = "Successful adding"
	
	return HttpResponse(export_list)

def saveReview(request,r_name,r_airline,r_mark):
	airline_exists = models.Airline.objects.filter(id_airline=r_airline)
	export_list = ""
	if not airline_exists.exists():
		export_list = "No such airline"
	else:
		airline_exists = models.Airline.objects.get(id_airline=r_airline)
		if (int(r_mark)>10): export_list = "Max mark is 10"
		else:
			newReview = models.Review.objects.create(human_name=r_name, airline=airline_exists, mark=int(r_mark))
			newReview.save()

			allReview = models.Review.objects.filter(airline=r_airline)
			sums=0
			for i in range(len(list(allReview))):
				sums = sums + int(allReview[i].mark)
			sums = sums/len(list(allReview))

			airline_exists.mark_sum = sums
			airline_exists.save()

			export_list = "Successful adding"

	return HttpResponse(export_list)

		
def getTickets(request,document):
	tickets = models.Ticket.objects.filter(human_document=document)
	export_list = ""
	if not tickets.exists():
		export_list = "You have no tickets"
	else:
		for i in range(len(list(tickets))):
			export_list = export_list + tickets[i].human_document.human_document + '/' + str(tickets[i].flight.id_flight) + '/' + tickets[i].place + '/' +  tickets[i].status + '/' + str(tickets[i].cost) + '/' + str(tickets[i].seq_num) + "<br>"

	return HttpResponse(export_list)



def saveTicket(request,in_login,flight):
	seat = ('ABCDEF')

	human = models.Human.objects.get(login=in_login)
	current_flight = models.Flight.objects.get(id_flight=flight)
	current_voyage = models.Voyage.objects.get(id_voyage=current_flight.voyage.id_voyage)
	city_f = models.Airport.objects.get(id_airport=current_voyage.airport_from.id_airport)
	city_t = models.Airport.objects.get(id_airport=current_voyage.airport_to.id_airport)

	newOrder = models.Order.objects.create(quantity=1,customer=human.full_name)
	newOrder.save()

	newTrip = models.Trip.objects.create(order_id=newOrder.id_order,city_from=city_f.full_name,city_to=city_t.full_name)
	newTrip.save()

	newPlace = str(random.randint(1,30)) + random.choice(seat)
	someRate = models.Rate.objects.get(id_rate=random.randrange(1,24))
	newTicket = models.Ticket.objects.create(human_document=human, flight=current_flight,
		place=newPlace,status='Оплачено',cost=random.randrange(1,100000,50),
		rate=someRate,trip_id=newTrip.id_trip,seq_num=str(1))
	newTicket.save()

	return HttpResponse("Successful buy")


def getTopAirlines(request):
	airlines = models.Airline.objects.all().order_by('-mark_sum')[:10]

	export_list=""
	for i in range(len(list(airlines))):
		export_list = export_list + airlines[i].id_airline + '/' + str(round(airlines[i].mark_sum,1)) + "<br>"

	return HttpResponse(export_list)
    
def changeInfo(request,id_docum,name,gen,email):
    human = models.Human.objects.get(human_document=id_docum)          
    human.full_name = name
    human.gender = gen
    human.email = email
    human.save()
    return HttpResponse("Successful change")
    
        

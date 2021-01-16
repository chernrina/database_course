from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from tables import views
from datetime import date

urlpatterns = [
    path('getLogin/<str:in_login>/', views.getLogin),
    path('getPassword/<str:in_login>/', views.getPassword),
    path('getHuman/<str:in_login>/', views.getHuman),
    path('getFlights/<str:city_from>/<str:city_to>/<str:date_f>/', views.getFlights),
    path('saveHuman/<str:doc>/<str:f_name>/<str:gen>/<str:mail>/<str:log>/<str:key>/', views.saveHuman),
    path('saveReview/<str:r_name>/<str:r_airline>/<str:r_mark>/', views.saveReview),
    path('getTickets/<str:document>/', views.getTickets),
    path('saveTicket/<str:in_login>/<str:flight>/', views.saveTicket),
    path('getTopAirlines/', views.getTopAirlines),
    path('changeInfo/<str:id_docum>/<str:name>/<str:gen>/<str:email>/',views.changeInfo),
]
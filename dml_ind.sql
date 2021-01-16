\c flight_db;

START TRANSACTION;

-- 1 Вывести людей, которые летают не менее 2-х раз в месяц за последний год.

select human_document, full_name from
(select human.human_document, full_name, extract(month from flight.date_from) as mon, count(*) as cnt
from human
inner join ticket on ticket.human_document = human.human_document
inner join flight on flight.id_flight = ticket.flight
where flight.date_from >= (current_date - integer '365')
group by human.human_document, full_name, extract(month from flight.date_from)
having count(*)>=2) as query
group by human_document, full_name
having count(*) = 12
\g 'dml_ind_res/1.txt'

-- 2 Вывести маршруты, на которых средняя заполняемость полетов менее 50%.

select id_voyage from voyage 
inner join flight on flight.voyage=voyage.id_voyage
inner join airplane on airplane.id_airplane=flight.airplane 
group by id_voyage 
having sum((select count(*) from ticket where flight=flight.id_flight)
/airplane.places)
/(select count(*) from flight where voyage=id_voyage)<0.5
\g 'dml_ind_res/2.txt'

COMMIT;
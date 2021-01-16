\c flight_db;

START TRANSACTION;

-- 1 Сделайте выборку всех данных из каждой таблицы

SELECT * FROM human; 
SELECT * FROM rate;
SELECT * FROM airline;
SELECT * FROM airplane;
SELECT * FROM airport;
SELECT * FROM review;
SELECT * FROM voyage;
SELECT * FROM flight;
SELECT * FROM timetable;
SELECT * FROM public.order;
SELECT * FROM trip;
SELECT * FROM ticket;

-- 2 Сделайте выборку данных из одной таблицы при нескольких условиях, с использованием логических операций, LIKE, BETWEEN, IN (не менее 3-х разных примеров)

SELECT id_airline,create_in
FROM airline
WHERE id_airline LIKE '%S%';

SELECT human_document,flight,cost
FROM ticket
WHERE cost BETWEEN 10000 AND 20000;

SELECT id_airline,mark_sum
FROM airline
WHERE mark_sum IN (4.4,4.5,4.6,4.7,4.8,4.9,5.0);

SELECT id_flight,voyage,airplane
FROM flight
WHERE airplane LIKE 'A%' AND voyage IN ('d13J4','I84c5');

-- 3 Создайте в запросе вычисляемое поле

SELECT id_order, quantity, (id_order*quantity) AS mult
FROM public.order;

-- 4 Сделайте выборку всех данных с сортировкой по нескольким полям

SELECT * FROM ticket
ORDER BY cost, trip_id ASC;

-- 5 Создайте запрос, вычисляющий несколько совокупных характеристик таблиц

SELECT AVG(cost) AS cost_avg, MAX(flight) AS max_flight
FROM ticket;

-- 6 Сделайте выборку данных из связанных таблиц (не менее двух примеров)

SELECT id_flight, voyage.airport_from AS from, voyage.airport_to AS to
FROM flight
INNER JOIN voyage ON voyage.id_voyage = flight.voyage;

SELECT ticket.human_document, human.full_name AS name, rate.baggage AS baggage
FROM ticket
LEFT JOIN rate ON rate.id_rate = ticket.rate
LEFT JOIN human ON human.human_document = ticket.human_document;

-- 7 Создайте запрос, рассчитывающий совокупную характеристику с использованием группировки, наложите ограничение на результат группировки 

SELECT id_voyage, airport.city AS city_from, airline.mark_sum AS markOfAirline
FROM voyage 
INNER JOIN airport ON airport.id_airport = voyage.airport_from
INNER JOIN airline ON airline.id_airline = voyage.airline
GROUP BY id_voyage, airport.city, airline.mark_sum
HAVING airline.mark_sum>5;

-- 8 Придумайте и реализуйте пример использования вложенного запроса

SELECT id_ticket, flight FROM ticket
WHERE flight IN
(SELECT id_flight FROM flight WHERE voyage LIKE '%70%');

-- 9 С помощью оператора INSERT добавьте в каждую таблицу по одной записи

INSERT INTO public.human (human_document, full_name, gender, email) VALUES ('1234 567891', 'Ivanov Ivan Ivanovich', 'M', 'ivan@mail.ru');

INSERT INTO public.rate (baggage, select_seat, class) VALUES ('Up to 1 kg', 'Can choose', 'Second');

INSERT INTO public.airline (id_airline, supervisor, create_in, mark_sum) VALUES ('Russia', 'Ivanov Ivan Ivanovich', '2020', '0');

INSERT INTO public.review (human_name, airline, mark) VALUES ('Ivanov Ivan Ivanovich', 'Russia', '10');

INSERT INTO public.airplane (id_airplane, places) VALUES ('Airbus A319', '150');

INSERT INTO public.airport (id_airport, city, full_name) VALUES ('AAB','City','Airport');

INSERT INTO public.voyage (id_voyage, airport_from, airport_to, airline) VALUES ('s1s00','LED','KZN','Russia');

INSERT INTO public.flight (voyage, date_from, date_to, airplane) VALUES ('s1s00','2020-04-16 05:25:00','2020-04-16 12:48:00','Boeing-737-900ER');

INSERT INTO public.timetable (date_timetable, voyage, flight) VALUES ('2020-04-16','s1s00',(SELECT COUNT(id_flight) FROM flight));

INSERT INTO public.order (quantity, customer) VALUES ('1','Ivanov Ivan Ivanovich');

INSERT INTO public.trip (order_id, city_from, city_to) VALUES ((SELECT COUNT(id_order) FROM public.order), (SELECT city FROM airport WHERE id_airport='LED'), (SELECT city FROM airport WHERE id_airport='KZN'));

INSERT INTO public.ticket (human_document,flight, place, status, cost, rate, trip_id, seq_num) VALUES ('1234 567891', (SELECT COUNT(id_flight) FROM flight), '1A', 'Paid', '7500', (SELECT COUNT(id_rate) from rate), (SELECT COUNT(id_trip) FROM trip), '1');

-- 10 С помощью оператора UPDATE измените значения нескольких полей у всех записей, отвечающих заданному условию

UPDATE ticket SET cost=15000 WHERE cost>70000 AND cost<90000;

-- 11 С помощью оператора DELETE удалите запись, имеющую максимальное (минимальное) значение некоторой совокупной характеристики

DELETE FROM ticket WHERE cost= ( SELECT MAX(cost) FROM ticket);

-- 12 С помощью оператора DELETE удалите записи в главной таблице, на которые не ссылается подчиненная таблица (используя вложенный запрос)

DELETE FROM human WHERE human_document NOT IN ( SELECT human_document FROM ticket GROUP BY human_document);



COMMIT;	
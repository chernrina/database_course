\c flight_db;

START TRANSACTION;

ALTER TABLE public.human
 ALTER COLUMN email TYPE VARCHAR(100);

ALTER TABLE public.ticket
 DROP CONSTRAINT rate_with_name;

CREATE SEQUENCE id_rate_seq;
 ALTER TABLE public.rate
  ALTER COLUMN id_rate SET DEFAULT nextval('id_rate_seq');

ALTER TABLE public.rate
 ALTER COLUMN select_seat TYPE VARCHAR(20);

ALTER TABLE public.rate
 ALTER COLUMN class TYPE VARCHAR(30);

CREATE SEQUENCE id_review_seq;
 ALTER TABLE public.review 
  ALTER COLUMN id_review SET DEFAULT nextval('id_review_seq');

ALTER TABLE public.airplane
 DROP COLUMN free_places;

ALTER TABLE public.airport
 DROP COLUMN address;

ALTER TABLE public.airport
 ALTER COLUMN city TYPE VARCHAR(100);

ALTER TABLE public.ticket
 DROP CONSTRAINT flight_with_id;
ALTER TABLE public.timetable
 DROP CONSTRAINT flight_with_name;

ALTER TABLE public.flight
 ALTER COLUMN id_flight TYPE INT USING id_flight::integer;

CREATE SEQUENCE id_flight_seq;
 ALTER TABLE public.flight
  ALTER COLUMN id_flight SET DEFAULT nextval('id_flight_seq');

ALTER TABLE public.ticket
 ALTER COLUMN flight TYPE INT USING flight::integer;

CREATE SEQUENCE id_ticket_seq;
 ALTER TABLE public.ticket
  ALTER COLUMN id_ticket SET DEFAULT nextval('id_ticket_seq');

ALTER TABLE public.timetable
 RENAME COLUMN date TO date_timetable;

ALTER TABLE public.timetable
 ALTER COLUMN date_timetable TYPE DATE;

CREATE SEQUENCE id_timetable_seq;
 ALTER TABLE public.timetable
  ALTER COLUMN id_timetable SET DEFAULT nextval('id_timetable_seq');

ALTER TABLE public.timetable
 ALTER COLUMN flight TYPE INT USING flight::integer;

CREATE SEQUENCE id_order_seq;
 ALTER TABLE public.order 
  ALTER COLUMN id_order SET DEFAULT nextval('id_order_seq');

ALTER TABLE public.trip
 ALTER COLUMN city_from TYPE VARCHAR(50);

ALTER TABLE public.trip
 ALTER COLUMN city_to TYPE VARCHAR(50);

CREATE SEQUENCE id_trip_seq;
 ALTER TABLE public.trip 
  ALTER COLUMN id_trip SET DEFAULT nextval('id_trip_seq');

ALTER TABLE public.ticket
 ADD CONSTRAINT flight_with_id
  FOREIGN KEY(flight)
  REFERENCES public.flight (id_flight)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE public.ticket
 ADD CONSTRAINT rate_with_name
  FOREIGN KEY(rate)
  REFERENCES public.rate (id_rate)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
ALTER TABLE public.timetable
 ADD CONSTRAINT flight_with_name
  FOREIGN KEY(flight)
  REFERENCES public.flight (id_flight)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

COMMIT;


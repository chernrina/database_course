DROP DATABASE IF EXISTS flight_db;

CREATE DATABASE flight_db;
\c flight_db;

START TRANSACTION;

CREATE TABLE IF NOT EXISTS public.human (
 human_document VARCHAR(25) NOT NULL,
 full_name VARCHAR(100) NOT NULL,
 gender CHAR NOT NULL,
 email VARCHAR(50) NULL,
 PRIMARY KEY (human_document))
;

CREATE TABLE IF NOT EXISTS public.rate (
 id_rate INT NOT NULL,
 baggage VARCHAR(50) NOT NULL,
 select_seat VARCHAR(10) NOT NULL,
 class CHAR NOT NULL,
 PRIMARY KEY (id_rate))
;

CREATE TABLE IF NOT EXISTS public.airline (
 id_airline VARCHAR(30) NOT NULL,
 create_in INT NOT NULL,
 supervisor VARCHAR(100) NOT NULL,
 mark_sum NUMERIC NOT NULL,
 PRIMARY KEY (id_airline))
;

CREATE TABLE IF NOT EXISTS public.review (
 id_review INT NOT NULL,
 human_name VARCHAR(100) NOT NULL,
 airline VARCHAR(30) NOT NULL,
 mark NUMERIC NOT NULL,
 PRIMARY KEY (id_review),
 CONSTRAINT airline_with_name
  FOREIGN KEY (airline)
  REFERENCES public.airline (id_airline) 
  ON DELETE NO ACTION
  ON UPDATE NO ACTION) 
;

CREATE TABLE IF NOT EXISTS public.airplane (
 id_airplane VARCHAR(30) NOT NULL,
 places INT NOT NULL,
 free_places INT NOT NULL,
 PRIMARY KEY(id_airplane))
;

CREATE TABLE IF NOT EXISTS public.airport (
 id_airport VARCHAR(10) NOT NULL,
 full_name VARCHAR(50) NOT NULL,
 city VARCHAR(50) NOT NULL,
 address VARCHAR(100) NOT NULL,
 PRIMARY KEY(id_airport))
;

CREATE TABLE IF NOT EXISTS public.voyage (
 id_voyage VARCHAR(10) NOT NULL,
 airport_from VARCHAR(10) NOT NULL,
 airport_to VARCHAR(10) NOT NULL,
 airline VARCHAR(30) NOT NULL,
 PRIMARY KEY (id_voyage),
 CONSTRAINT from_with_airport
  FOREIGN KEY(airport_from)
  REFERENCES public.airport (id_airport) 
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
 CONSTRAINT to_with_airport
  FOREIGN KEY(airport_to)
  REFERENCES public.airport (id_airport) 
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
 CONSTRAINT airline_with_name
  FOREIGN KEY(airline)
  REFERENCES public.airline(id_airline) 
  ON DELETE NO ACTION
  ON UPDATE NO ACTION)
;

CREATE TABLE IF NOT EXISTS public.flight (
 id_flight VARCHAR(10) NOT NULL,
 voyage VARCHAR(10) NOT NULL,
 date_from TIMESTAMP NOT NULL,
 date_to TIMESTAMP NOT NULL,
 airplane VARCHAR(30) NOT NULL,
 PRIMARY KEY (id_flight),
 CONSTRAINT airplane_with_name
  FOREIGN KEY(airplane)
  REFERENCES public.airplane (id_airplane) 
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
 CONSTRAINT voyage_with_name
  FOREIGN KEY(voyage)
  REFERENCES public.voyage (id_voyage) 
  ON DELETE NO ACTION
  ON UPDATE NO ACTION)
;

CREATE TABLE IF NOT EXISTS public.ticket (
 id_ticket INT NOT NULL,
 human_document VARCHAR(25) NOT NULL,
 flight VARCHAR(15) NOT NULL,
 place VARCHAR(5) NOT NULL,
 status CHAR(15) NULL,
 cost NUMERIC NULL,
 rate INT NULL,
 PRIMARY KEY (id_ticket),
 CONSTRAINT document_with_human
  FOREIGN KEY(human_document)
  REFERENCES public.human (human_document)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
 CONSTRAINT rate_with_name
  FOREIGN KEY(rate)
  REFERENCES public.rate (id_rate)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
 CONSTRAINT flight_with_id
  FOREIGN KEY(flight)
  REFERENCES public.flight (id_flight)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION)
;

CREATE TABLE IF NOT EXISTS public.timetable (
 id_timetable INT NOT NULL,
 date TIMESTAMP NOT NULL,
 voyage VARCHAR(10) NOT NULL,
 flight VARCHAR(10) NOT NULL,
 PRIMARY KEY (id_timetable),
 CONSTRAINT voyage_with_name
  FOREIGN KEY(voyage)
  REFERENCES public.voyage (id_voyage)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
 CONSTRAINT flight_with_name
  FOREIGN KEY(flight)
  REFERENCES public.flight (id_flight)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION)
;

COMMIT;
\c flight_db;

START TRANSACTION;

ALTER TABLE public.human
 ADD login VARCHAR NULL;

ALTER TABLE public.human
 ADD password VARCHAR NULL;

COMMIT;
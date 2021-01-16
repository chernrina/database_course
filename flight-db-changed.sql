\c flight_db;

START TRANSACTION;

DROP TABLE IF EXISTS public.order;

CREATE TABLE IF NOT EXISTS public.order ( 
  id_order INT NOT NULL,
  quantity INT NOT NULL,
  customer VARCHAR(100) NOT NULL,
  PRIMARY KEY (id_order)
);

DROP TABLE IF EXISTS public.trip;

CREATE TABLE IF NOT EXISTS public.trip ( 
  id_trip INT NOT NULL,
  order_id INT NOT NULL,
  city_from VARCHAR(30) NOT NULL,
  city_to VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_trip),
  CONSTRAINT order_with_order_id
  FOREIGN KEY(order_id)
  REFERENCES public.order (id_order)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
);

ALTER TABLE public.ticket ADD
  trip_id INT NOT NULL;

ALTER TABLE public.ticket ADD
  seq_num INT NOT NULL; 

ALTER TABLE public.ticket ADD
  CONSTRAINT trip_with_trip_id
  FOREIGN KEY(trip_id)
  REFERENCES public.trip (id_trip)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

COMMIT;
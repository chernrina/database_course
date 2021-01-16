from django.db import models


class Airline(models.Model):
    id_airline = models.CharField(primary_key=True, max_length=30)
    create_in = models.IntegerField()
    supervisor = models.CharField(max_length=100)
    mark_sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'airline'


class Airplane(models.Model):
    id_airplane = models.CharField(primary_key=True, max_length=30)
    places = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'airplane'


class Airport(models.Model):
    id_airport = models.CharField(primary_key=True, max_length=10)
    full_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'airport'


class Flight(models.Model):
    id_flight = models.AutoField(primary_key=True)
    voyage = models.ForeignKey('Voyage', models.DO_NOTHING, db_column='voyage')
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, models.DO_NOTHING, db_column='airplane')

    class Meta:
        managed = False
        db_table = 'flight'


class Human(models.Model):
    human_document = models.CharField(primary_key=True, max_length=25)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=100, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'human'


class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    customer = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'order'


class Rate(models.Model):
    id_rate = models.AutoField(primary_key=True)
    baggage = models.CharField(max_length=50)
    select_seat = models.CharField(max_length=20)
    class_field = models.CharField(db_column='class', max_length=30)  

    class Meta:
        managed = False
        db_table = 'rate'


class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    human_name = models.CharField(max_length=100)
    airline = models.ForeignKey(Airline, models.DO_NOTHING, db_column='airline')
    mark = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'review'


class Ticket(models.Model):
    id_ticket = models.AutoField(primary_key=True)
    human_document = models.ForeignKey(Human, models.DO_NOTHING, db_column='human_document')
    flight = models.ForeignKey(Flight, models.DO_NOTHING, db_column='flight')
    place = models.CharField(max_length=5)
    status = models.CharField(max_length=15, blank=True, null=True)
    cost = models.IntegerField()
    rate = models.ForeignKey(Rate, models.DO_NOTHING, db_column='rate', blank=True, null=True)
    trip = models.ForeignKey('Trip', models.DO_NOTHING)
    seq_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket'


class Timetable(models.Model):
    id_timetable = models.AutoField(primary_key=True)
    date_timetable = models.DateField()
    voyage = models.ForeignKey('Voyage', models.DO_NOTHING, db_column='voyage')
    flight = models.ForeignKey(Flight, models.DO_NOTHING, db_column='flight')

    class Meta:
        managed = False
        db_table = 'timetable'


class Trip(models.Model):
    id_trip = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING)
    city_from = models.CharField(max_length=50)
    city_to = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'trip'


class Voyage(models.Model):
    id_voyage = models.CharField(primary_key=True, max_length=10)
    airport_from = models.ForeignKey(Airport, models.DO_NOTHING, related_name="airport_start", db_column='airport_from')
    airport_to = models.ForeignKey(Airport, models.DO_NOTHING, db_column='airport_to')
    airline = models.ForeignKey(Airline, models.DO_NOTHING, db_column='airline')

    class Meta:
        managed = False
        db_table = 'voyage'

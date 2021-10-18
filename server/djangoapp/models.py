from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=16, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    BODY_TYPES = [
        ('coupe', 'coupe'), 
        ('sedan', 'sedan'), 
        ('wagon', 'wagon'), 
        ('suv', 'SUV'), 
        ('van', 'van')
    ]
    name = models.CharField(max_length=32, null=False)
    dealerId = models.IntegerField(null=False)
    body_type = models.CharField(max_length=11, choices=BODY_TYPES, null=False)
    year = models.DateField(null=False)

    def __str__(self):
        return self.make + self.name + self.year


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, dealership, purchase, purchase_date, car_make, 
    car_model, car_year, name, review, sentiment):
        self.id = id
        self.dealership = dealership
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.name = name
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review

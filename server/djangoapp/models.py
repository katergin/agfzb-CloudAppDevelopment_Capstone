import json
from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=16, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return f"{self.name}"


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
        return f"{self.make} {self.name} {str(self.year)}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, purchase, purchase_date, car_make, 
    car_model, car_year, name, review, sentiment):
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

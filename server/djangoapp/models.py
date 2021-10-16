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


# <HINT> Create a plain Python class `DealerReview` to hold review data

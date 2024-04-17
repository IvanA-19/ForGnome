from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    img = models.TextField()

    def __str__(self):
        return self.name


class DrinkPositions(models.Model):
    place = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField()
    price = models.FloatField()
    img = models.TextField()

    def __str__(self):
        return self.name


class FoodPositions(models.Model):
    place = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField()
    price = models.FloatField()
    img = models.TextField()

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField()

    def __str__(self):
        return self.address


class Order(models.Model):
    position = models.CharField(max_length=200)
    price = models.FloatField()
    count = models.IntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.position

from django.db import models

# Create your models here.

class User (models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    password = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)


class Car(models.Model):
    model = models.CharField(max_length=50, null=False)
    registration_number = models.CharField(max_length=50, null=False, unique=True)
    hire = models.BooleanField(max_length=50, null=False)
    sale = models.BooleanField(max_length=50, null=False)
    user_id = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, default='')
    available = models.BooleanField(null=False, default=True)
    created = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    car_id = models.CharField(max_length=50, null=False)
    user_id = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, default='')
    paid = models.BooleanField(null=False, default=False)
    collected = models.BooleanField(null=False, default=False)
    returned = models.BooleanField(null=False, default=False)
    date_returned = models.DateTimeField(auto_now_add=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

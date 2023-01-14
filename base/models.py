from django.db import models

# Create your models here.

class User(models.Model):
    USERNAME_FIELD = 'email'
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
    count = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)

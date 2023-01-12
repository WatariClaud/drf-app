from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False, default='null_email')
    password = models.CharField(max_length=255, null=False, default='invalid_password')
    profession = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
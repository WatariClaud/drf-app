from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    profession = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
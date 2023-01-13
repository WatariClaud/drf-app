from django.db import models

# Create your models here.

class User(models.Model):
    USERNAME_FIELD = 'email'
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    password = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)

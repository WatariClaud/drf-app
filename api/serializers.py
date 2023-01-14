from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Car

class UserSerializer_SignUp(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined']

class UserSerializer_SignIn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserSerializer_Authed(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined']
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined']
        # fields = '__all__'

class CarSerializer_View(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        
class CarSerializer_Add(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['model', 'registration_number', 'count']
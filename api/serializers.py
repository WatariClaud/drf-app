from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Car, Booking

class UserSerializer_SignUp(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'email', 'password', 'is_active', 'date_joined']
        fields = '__all__'

class UserSerializer_SignIn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserSerializer_Authed(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined']


class UserSerializer_Searched(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CarSerializer_View_Self(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'model', 'registration_number', 'hire', 'sale', 'description', 'available', 'created']
       
class CarSerializer_View(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'user_id', 'model', 'registration_number', 'hire', 'sale', 'description', 'available', 'created']
        
class CarSerializer_Add(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['model', 'registration_number']

class BookingSerializer_View(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'car_id', 'user_id', 'description', 'collected', 'created', 'paid', 'returned']
        
class BookingSerializer_Add(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'car_id', 'user_id', 'description', 'paid', 'returned', 'collected']
        
class BookingSerializer_Update(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'paid', 'returned', 'date_returned']
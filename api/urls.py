from django.urls import path
from . import auth, cars

urlpatterns = [
    path('data', auth.get_data),
    path('add', auth.add_user),
    path('login', auth.auth_user),
    path('cars/view', cars.get_cars),
    path('cars/add', cars.add_car),
]
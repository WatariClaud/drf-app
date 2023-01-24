from django.urls import path
from . import auth, cars, booking

urlpatterns = [
    path('data', auth.get_data),
    path('add', auth.add_user),
    path('login', auth.auth_user),
    path('user/search', auth.get_user),
    path('cars/add', cars.add_car),
    path('cars/view', cars.get_cars),
    path('cars/update/id=<car_id>', cars.update_car_details),
    path('cars/view/id=<car_id>', cars.get_car_by_id),
    path('cars/search', cars.search_by_model),
    path('cars/book/<car_id>', booking.make_booking),
    path('bookings', booking.get_bookings),
    path('bookings/confirm/<booking_id>', booking.confirm_booking),
]
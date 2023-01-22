from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.admin import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import CarSerializer_View, UserSerializer_Authed, BookingSerializer_Add, BookingSerializer_Update, BookingSerializer_View
from base.models import Car, Booking

@api_view(['POST'])
def make_booking(request, car_id):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    user_id = user.data.get('id')
    user_name = user.data.get('username')
    description = request.data.get('description')
    res = {
        "message": "invalid car id"
    }
    car_result: Car
    try:
        if car_id.isdigit():
            if not Car.objects.filter(id=car_id):
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                car_result = Car.objects.filter(id=car_id).get()
        else:
            if not Car.objects.filter(registration_number=car_id):
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                car_result = Car.objects.filter(registration_number=car_id).get()
        car = CarSerializer_View(car_result)
        car_id = car.data.get('id')
        if description is None or not description and description == '':
            description = user_name + ' booked car number ' + str(car_id)
        booking = Booking.objects.create(car_id=car_id, user_id=user_id, description=description, paid=False, returned=False, collected=False)
        print('three')
        res = {
            "message": "Booked successfully",
            "booking_id": booking.pk
        }
        return Response(res, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    return
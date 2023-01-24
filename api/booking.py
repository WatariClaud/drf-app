from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CarSerializer_View, UserSerializer_Authed, BookingSerializer_View
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
        car_user_id = car.data.get('user_id')
        if description is None or not description and description == '':
            description = user_name + ' booked car number ' + str(car_id)
        if car_user_id == str(user_id):
            res = {
                "message": "cannot book own car"
            }
            return Response(res, status=status.HTTP_409_CONFLICT)
        booking = Booking.objects.create(car_id=car_id, user_id=user_id, description=description, paid=False, returned=False, collected=False)
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

@api_view(['PATCH'])
def confirm_booking(request, booking_id):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    user_id = user.data.get('id')

    try:
        booking = Booking.objects.filter(id=booking_id).get()
        booking_serialized = BookingSerializer_View(booking)
        car = Car.objects.filter(id=booking_serialized.data.get('car_id')).get()
        print(car.user_id, str(user_id))
        if car.user_id != str(user_id):
            res = {
                "message": "Unauthorized request"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        if booking.collected == True:
            res = {
                "message": "Booking already confirmed"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        booking.id = booking_id
        booking.collected = True
        booking.paid = True
        booking.returned = False
        booking.save()
        res = {
            "message": "confirmed booking successfully",
            "booking_id": booking.id
        }
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_bookings(request):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    user_id = user.data.get('id')
    sort = request.GET.get('sort', 'all')
    bookings: Booking
    try:
        if sort == 'all':
            bookings = Booking.objects.filter(user_id=str(user_id)).order_by('-id')
        elif sort == 'collected':
            bookings = Booking.objects.filter(user_id=str(user_id), collected=True, returned=False).order_by('-id')
        elif sort == 'returned':
            bookings = Booking.objects.filter(user_id=str(user_id), returned=True).order_by('-id')
        else:
            res = {
                "message": "invalid sort query"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        bookings_serialized = BookingSerializer_View(bookings, many=True)
        res = {
            "message": "bookings",
            "data": bookings_serialized.data
        }
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

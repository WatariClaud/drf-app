from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import status
from base.models import Car
from .serializers import CarSerializer_View, CarSerializer_Add, UserSerializer_Authed
from django.core import serializers

@api_view(['GET'])
def get_cars(request):
    cars = Car.objects.all()
    authed_user = TokenAuthentication().authenticate(request)
    serializer = UserSerializer_Authed(authed_user[0])
    user_id = serializer.data.get('id')
    user_cars = cars.filter(user_id=user_id)
    car_serialier = CarSerializer_View(user_cars, many=True)
    return Response(car_serialier.data)

@api_view(['POST'])
def add_car(request):
    serializer = CarSerializer_Add(data = request.data)
    is_valid = serializer.is_valid()
    errors = serializer.errors
    model = request.data.get('model')
    registration_number = request.data.get('registration_number')
    sale_or_hire = request.data.get('sale_or_hire')
    count = request.data.get('count')
    authed_user = TokenAuthentication().authenticate(request)
    serializer = UserSerializer_Authed(authed_user[0])
    user_id = serializer.data.get('id')
    sale= False
    hire = False
    try:
        if is_valid:
            if sale_or_hire == None or not (sale_or_hire == 'sale' and sale_or_hire != 'hire'):
                response = {
                    "message": "Invalid 'sale_or_hire' value",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            if sale_or_hire == 'hire':
                hire = True
                sale = False
            elif sale_or_hire == 'sale':
                sale = True
                hire = False
            car = Car.objects.create(model=model, registration_number=registration_number, sale=sale, hire=hire, user_id=user_id, count=count)
            # car.save()
            response = {
                "message": "Added successfully",
                "car_id": car.pk
            }
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = {
                "message": "An error occurred",
                "error": errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        response = {
            "message": "An error occured",
            "error": str(e)
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import status
from base.models import User
from .serializers import UserSerializer

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request):
    permission_classes = [IsAuthenticated]
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_user(request):
    serializer = UserSerializer(data = request.data)
    is_valid = serializer.is_valid()
    email = serializer.data.get('email')
    user = User.objects.get(email=email)
    if user is not None:
        response = {
            "message": "User already exists",
        }
        return Response(response, status=status.HTTP_412_PRECONDITION_FAILED)
    if is_valid:
        serializer.save()
        response = {
            "message": "Added successfully",
        }
        return Response(response, status=status.HTTP_201_CREATED)
    else:
        response = {
            "message": "An error occured"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def auth_user(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user= authenticate(email=email, password=password)
    if user is not None:
        response = {
            "message": "Authenticated successfully",
            "token": user.auth_token.key
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            "message": "Incorrect email or password"
        }
        return Response(response, status=status.HTTP_409_CONFLICT)
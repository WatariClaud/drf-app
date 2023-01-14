from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import status
# from base.models import User
from .serializers import UserSerializer_SignUp, UserSerializer_SignIn, UserSerializer_Authed
from django.core import serializers

def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
        # return user
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None

@api_view(['GET'])
def get_data(request):
    authed_user = TokenAuthentication().authenticate(request)
    serializer = UserSerializer_Authed(authed_user[0])
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_user(request):
    serializer = UserSerializer_SignUp(data = request.data)
    is_valid = serializer.is_valid()
    errors = serializer.errors
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = ''
    last_name = ''
    if len(username.split(' ')) > 1:
        first_name = username.split(' ')[0]
        last_name = username.split(' ')[1]
    user = authenticate_user(email, password)
    if user is not None:
        response = {
            "message": "User already exists",
        }
        return Response(response, status=status.HTTP_412_PRECONDITION_FAILED)
    else:
        try:
            if is_valid:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                token = Token.objects.create(user=user)
                response = {
                    "message": "Added successfully",
                    "token": token.key
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

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def auth_user(request):
    serializer = UserSerializer_SignIn(data = request.data)
    is_valid = serializer.is_valid()
    errors = serializer.errors
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate_user(email, password)
    try:
        if is_valid:
            if user is not None:
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                response = {
                    "message": "Authenticated successfully",
                    "token": token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "message": "Incorrect email or password"
                }
                return Response(response, status=status.HTTP_409_CONFLICT)
        else :
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




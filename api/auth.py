from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.admin import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from .serializers import UserSerializer_SignUp, UserSerializer_SignIn, UserSerializer_Authed, UserSerializer_Searched

def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def add_user(request):
    serialized = UserSerializer_SignUp(data=request.data)
    is_valid = serialized.is_valid()
    errors = serialized.errors
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if username is None or email is None or password is None:
            res = {
                "username": "this field is required",
                "email": "this field is required",
                "password": "this field is required"
            }
            return Response(res, status=status.HTTP_409_CONFLICT)

        if is_valid:
            existing = authenticate_user(email, password)
            if existing is not None:
                res = {
                    "message": "checking what went wrong....",
                    "error": {
                        "email": [
                            "A user with that email already exists."
                        ]
                    }
                }
                return Response(res, status=status.HTTP_412_PRECONDITION_FAILED)
            user = User.objects.create_user(username, email, password)
            token = Token.objects.create(user=user)
            res = {
                "message": "created successfully",
                "token": token.key
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "message": "something went wrong....",
                "error": errors
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def auth_user(request):
    serialized = UserSerializer_SignIn(data=request.data)
    is_valid = serialized.is_valid()
    errors = serialized.errors
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            res = {
                "email": "this field is required",
                "password": "this field is required"
            }
            return Response(res, status=status.HTTP_409_CONFLICT)

        if is_valid:
            existing = authenticate_user(email, password)
            if existing is None:
                res = {
                    "message": "something went wrong....",
                    "error": {
                        "email_password": [
                            "Incorrect credentials."
                        ]
                    }
                }
                return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            Token.objects.filter(user_id=existing).delete()
            token = Token.objects.create(user=existing)
            res = {
                "message": "authenticated successfully",
                "token": token.key
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "message": "something went wrong....",
                "error": errors
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_data(request):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    try:
        res = {
            "data": user.data
        }
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
      
@api_view(['GET'])
def get_user(request):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    logged_in_user_id = user.data.get('id')
    user_id = request.GET.get('user_id', logged_in_user_id)
    try:
        if not User.objects.filter(id=user_id):
            res = {
                "message": "invalid user id"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        user_to_search = User.objects.filter(id=user_id).get()
        search_result = UserSerializer_Searched(user_to_search)
        if str(logged_in_user_id) == str(user_id):
            res = {
                "data": user.data
            }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "data": search_result.data
            }
            return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
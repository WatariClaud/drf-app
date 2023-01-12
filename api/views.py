from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import User
from .serializers import UserSerializer

@api_view(['GET'])
def get_data(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response({
            "error": str(serializer.errors)
        })
    return Response(serializer.data)
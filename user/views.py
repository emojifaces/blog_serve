from rest_framework.response import Response
from rest_framework import viewsets
from user.models import User
from user.serializers import UserInfoSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

from rest_framework.response import Response
from rest_framework import viewsets
from user.models import User
from user.serializers import UserInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

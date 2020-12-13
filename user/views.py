from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from user.models import User
from user.serializers import UserInfoSerializer, MyTokenObtainPairSerializer, UserRegisterSerializer, \
    ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from common.utils import APIResponse, get_token_for_user
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class MyTokenObtainPairView(TokenObtainPairView):
    """
    自定义JWT登录
    """
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserInfoSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['update', 'change_password']:
            return [IsAuthenticated()]
        else:
            return []

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegisterSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        else:
            return UserInfoSerializer

    def update(self, request, *args, **kwargs):
        """
        修改用户信息
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save()
        return APIResponse(1, 'ok', data=serializer.data)

    @action(detail=False, methods=['POST'])
    def register(self, request, *args, **kwargs):
        """
        用户注册
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        user = serializer.save()
        jwt = get_token_for_user(user)
        user_info = UserInfoSerializer(user, context={'request': request}).data
        user_info.update(jwt)
        return APIResponse(1, 'ok', data=user_info)

    @action(detail=False, methods=['POST'])
    def change_password(self, request, *args, **kwargs):
        """
        修改用户密码
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save()
        return APIResponse(1, 'ok')

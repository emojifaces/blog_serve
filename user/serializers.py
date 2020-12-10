from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from user.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'user_head', 'weibo', 'profile', 'sex')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        request = self.context['request']

        user_head_url = f'{request.scheme}://{request.get_host()}{self.user.user_head.url}'
        data['userInfo'] = {
            'id': self.user.id,
            'nickname': self.user.nickname,
            'weibo': self.user.weibo,
            'profile': self.user.profile,
            'sex': self.user.get_sex_display(),
            'user_head': user_head_url,
        }
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

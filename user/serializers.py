from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from user.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """

    class Meta:
        model = User
        fields = ('id', 'nickname', 'user_head', 'weibo', 'profile', 'sex', 'email')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.user_head = validated_data.get('user_head', instance.user_head)
        instance.weibo = validated_data.get('weibo', instance.weibo)
        instance.profile = validated_data.get('profile', instance.weibo)
        instance.sex = validated_data.get('sex', instance.sex),
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    code = serializers.CharField(max_length=10, required=True)  # 注册邀请码

    class Meta:
        model = User
        fields = ('username', 'password', 'code')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
        }

    def validate_code(self, data):
        if data != '100033':
            raise serializers.ValidationError('邀请码错误！')
        return data

    def create(self, validated_data):
        del validated_data['code']
        try:
            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.nickname = validated_data['username']
            user.save()
        except:
            raise serializers.ValidationError('注册失败')
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义JWT序列化器
    """

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

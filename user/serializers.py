from user.models import User
from rest_framework import serializers

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('nickname','user_head','weibo','profile')


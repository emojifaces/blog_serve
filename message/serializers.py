from rest_framework import serializers
from message.models import Message
from user.serializers import UserInfoSerializer


class MessageSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    images = serializers.StringRelatedField(many=True)

    class Meta:
        model = Message
        fields = ('user', 'content', 'images', 'create_time')

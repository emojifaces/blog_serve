from rest_framework import serializers
from message.models import Message, MessageImg
from user.serializers import UserInfoSerializer


class MessageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageImg
        fields = ('id', 'img')


class MessageSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    images = MessageImageSerializer(many=True, read_only=True)
    imgs = serializers.ListField(write_only=True, required=False, child=serializers.ImageField())
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Message
        fields = ('id', 'user', 'content', 'images', 'create_time', 'imgs')
        read_only_fields = ('id',)

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        imgs = validated_data.pop('imgs', None)
        message = Message.objects.create(user=owner, **validated_data)
        if imgs:
            for img in imgs:
                MessageImg.objects.create(message=message, img=img)
        return message

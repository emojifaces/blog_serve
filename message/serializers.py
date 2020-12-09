from rest_framework import serializers
from message.models import Message, MessageImg
from user.serializers import UserInfoSerializer


class MessageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageImg
        fields = ('id', 'img')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class MessageSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    images = MessageImageSerializer(many=True, read_only=True)
    imgs = serializers.ListField(write_only=True, required=False, child=serializers.ImageField())
    is_mine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'user', 'content', 'images', 'create_time', 'imgs', 'is_mine')
        read_only_fields = ('id', 'user', 'create_time')
        extra_kwargs = {
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'content': {'required': True}
        }

    def get_is_mine(self, instance):
        request = self.context.get('request')
        return True if request.user == instance.user else False

    def validate(self, attrs):
        if not attrs.get('content'):
            raise serializers.ValidationError('content字段不能为空')
        return attrs

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        imgs = validated_data.pop('imgs', None)
        message = Message.objects.create(user=owner, **validated_data)
        if imgs:
            for img in imgs:
                MessageImg.objects.create(message=message, img=img)
        return message

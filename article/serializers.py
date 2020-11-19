from rest_framework import serializers
from article.models import Article
from user.serializers import UserInfoSerializer


class ArticleSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'create_time', 'img')
        read_only_fields = ('id', 'user', 'create_time')
        extra_kwargs = {
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'title': {'required': True},
            'content': {'required': True},
            'img': {'required': False}
        }

    def validate(self, attrs):
        if not attrs.get('title'):
            raise serializers.ValidationError('title字段不能为空')
        if not attrs.get('content'):
            raise serializers.ValidationError('content字段不能为空')
        if not attrs.get('img'):
            raise serializers.ValidationError('img字段不能为空')
        return attrs

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        return article

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.img = validated_data.get('img', instance.img)
        instance.save()
        return instance

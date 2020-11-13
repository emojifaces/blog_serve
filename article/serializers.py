from rest_framework import serializers
from article.models import Article
from user.serializers import UserInfoSerializer


class ArticleSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content')
        read_only_fields = ('id',)

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        return article

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

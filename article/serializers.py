import re
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
            'create_time': {'format': '%Y-%m-%d %H:%M'},
            'title': {'required': True},
            'content': {'required': True},
            'img': {'required': False}
        }

    def validate(self, attrs):
        if not attrs.get('title'):
            raise serializers.ValidationError('title字段不能为空')
        if not attrs.get('content'):
            raise serializers.ValidationError('content字段不能为空')
        return attrs

    def create(self, validated_data):
        try:
            article = Article.objects.create(**validated_data)
        except:
            raise serializers.ValidationError('创建失败')
        return article

    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.img = validated_data.get('img', instance.img)
            instance.save()
        except:
            raise serializers.ValidationError('保存失败')
        return instance


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'create_time', 'img', 'is_mine')
        read_only_fields = ('id', 'title', 'create_time', 'img')
        extra_kwargs = {
            'create_time': {'format': '%Y-%m-%d %H:%M'}
        }

    def get_content(self, instance):
        pre = re.compile(r'>(.*?)<')
        content_s = ''.join(pre.findall(instance.content))
        content_s = content_s.replace(u'&nbsp;', ' ')
        return content_s[0:20]

    def get_is_mine(self, instance):
        request = self.context.get('request')
        return True if request.user == instance.user else False

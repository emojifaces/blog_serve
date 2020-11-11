from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from article.models import Article
from article.serializers import ArticleSerializer


class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Article.objects.filter(is_delete=False)
    serializer_class = ArticleSerializer

    # def list(self, request, *args, **kwargs):
    #     """
    #         文章列表
    #     """
    #     articles = self.get_queryset()
    #     serializer = self.get_serializer(articles,many=True)
    #     return Response(serializer.data)

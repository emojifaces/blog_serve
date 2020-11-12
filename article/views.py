from rest_framework import viewsets
from common.utils import APIResponse
from rest_framework import mixins
from article.models import Article
from article.serializers import ArticleSerializer


class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Article.objects.filter(is_delete=False)
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        """
        文章列表
        """
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return APIResponse(1, 'ok', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        文章详情
        """
        article = self.get_object()
        serializer = self.get_serializer(article)
        return APIResponse(1, 'ok', serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        删除文章(逻辑删除)
        """
        article = self.get_object()
        article.is_delete = True
        article.save()
        return APIResponse(1, 'ok')

from rest_framework import viewsets
from common.utils import APIResponse
from rest_framework import mixins
from article.models import Article
from article.serializers import ArticleSerializer, ArticleListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Article.objects.filter(is_delete=False).order_by('-create_time')
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        重写权限规则
        """
        if self.action in ['create', 'update']:
            return [IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action in ['list']:
            return ArticleListSerializer
        else:
            return ArticleSerializer

    def list(self, request, *args, **kwargs):
        """
        文章列表
        """
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True, context={'request': request})
        return APIResponse(1, 'ok', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        文章详情
        """
        article = self.get_object()
        serializer = self.get_serializer(article)
        return APIResponse(1, 'ok', serializer.data)

    def create(self, request, *args, **kwargs):
        """
        新建文章
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save(user=request.user)
        return APIResponse(1, 'ok')

    def update(self, request, *args, **kwargs):
        """
        更新文章
        """
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data, partial=True)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save()
        return APIResponse(1, 'ok')

    def destroy(self, request, *args, **kwargs):
        """
        删除文章(逻辑删除)
        """
        article = self.get_object()
        article.is_delete = True
        article.save()
        return APIResponse(1, 'ok')

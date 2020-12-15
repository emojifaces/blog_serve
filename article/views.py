from rest_framework import viewsets
from rest_framework.decorators import action
from article.pagination import ArticlePageNumberPagination
from common.utils import APIResponse
from rest_framework import mixins
from article.models import Article
from article.serializers import ArticleSerializer, ArticleListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Article.objects.filter(is_delete=False).order_by('-create_time').all()
    authentication_classes = [JWTAuthentication]
    pagination_class = ArticlePageNumberPagination

    def get_permissions(self):
        """
        重写权限规则
        """
        if self.action in ['create', 'update', 'destroy', 'update_article', 'delete']:
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
        page = self.paginate_queryset(articles)
        if not page:
            return APIResponse(0, '暂时没有更多动态')
        serializer = self.get_serializer(page, many=True, context={'request': request})
        count = {'count': articles.count()}
        return APIResponse(1, 'ok', serializer.data, **count)

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
        return APIResponse(1, 'ok', data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        更新文章
        """
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data, partial=True)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save()
        return APIResponse(1, 'ok', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        删除文章(逻辑删除)
        """
        article = self.get_object()
        try:
            article.is_delete = True
            article.save()
        except:
            return APIResponse(0, '删除失败')
        return APIResponse(1, 'ok')

    @action(detail=True, methods=['POST'])
    def update_article(self, request, *args, **kwargs):
        """
        当前用户编辑自己的文章
        """
        article = self.get_object()
        if article.user != request.user:
            return APIResponse(0, '没有权限')
        serializer = self.get_serializer(article, data=request.data, partial=True)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save()
        return APIResponse(1, 'ok', data=serializer.data)

    @action(detail=True, methods=['POST'])
    def delete(self, request, *args, **kwargs):
        """
        当前用户删除自己的文章
        """
        article = self.get_object()
        if article.user != request.user:
            return APIResponse(0, '没有权限')
        try:
            article.is_delete = True
            article.save()
        except:
            return APIResponse(0, '删除失败')
        return APIResponse(1, 'ok')

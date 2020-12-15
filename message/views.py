from rest_framework import viewsets
from rest_framework.decorators import action

from message.models import Message
from message.serializers import MessageSerializer
from rest_framework import mixins
from common.utils import APIResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class MessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Message.objects.filter(is_delete=False).order_by('-create_time')
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def list(self, request, *args, **kwargs):
        """
        动态消息列表
        """
        messages = self.get_queryset()
        page = self.paginate_queryset(messages)
        if not page:
            return APIResponse(0, '暂时没有更多文章')
        serializer = self.get_serializer(page, many=True, context={'request': request})
        return APIResponse(1, 'ok', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        动态消息详情
        """
        message = self.get_object()
        serializer = self.get_serializer(message)
        return APIResponse(1, 'ok', serializer.data)

    def create(self, request, *args, **kwargs):
        """
        创建动态消息
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse(0, serializer.errors)
        serializer.save(owner=request.user)
        return APIResponse(1, 'ok', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        删除动态消息
        """
        message = self.get_object()
        message.is_delete = True
        message.save()
        return APIResponse(1, 'ok')

    @action(detail=True, methods=['POST'])
    def delete(self, request, *args, **kwargs):
        """
        删除当前登录用户自己的动态消息
        """
        message = self.get_object()
        if message.user != request.user:
            return APIResponse(0, '没有权限')
        try:
            message.is_delete = True
            message.save()
        except:
            return APIResponse(0, '删除失败')
        return APIResponse(1, 'ok')

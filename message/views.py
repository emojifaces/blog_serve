from rest_framework import viewsets
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
        if self.action in ['create', 'update']:
            return [IsAuthenticated()]
        return []

    def list(self, request, *args, **kwargs):
        """
        动态消息列表
        """
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
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
        return APIResponse(1, 'ok')

    def destroy(self, request, *args, **kwargs):
        """
        删除动态消息
        """
        message = self.get_object()
        message.is_delete = True
        message.save()
        return APIResponse(1, 'ok')

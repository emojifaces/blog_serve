from rest_framework import viewsets
from message.models import Message
from message.serializers import MessageSerializer
from rest_framework import mixins
from common.utils import APIResponse


class MessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Message.objects.filter(is_delete=False)
    serializer_class = MessageSerializer

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

    def destroy(self, request, *args, **kwargs):
        """
        删除动态消息
        """
        message = self.get_object()
        message.is_delete = True
        message.save()
        return APIResponse(1, 'ok')

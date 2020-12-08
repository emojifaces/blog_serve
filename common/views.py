from django.utils import timezone
import datetime
import os

from django.db.models import Q
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import uuid

from article.models import Article
from message.models import Message
from myblog_serve.settings import MEDIA_ROOT, MEDIA_URL
from common.utils import APIResponse
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_upload_img(request):
    """
    文章内容图片上传
    :param request:
    :return: { "location" : "/demo/image/1.jpg" }
    """
    data = request.data
    file = data.get('file')
    file_suffix = file.name.split('.')[-1]
    file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_suffix
    directory = os.path.join(MEDIA_ROOT, 'article')
    if not os.path.exists(directory):
        os.mkdir(directory)
    file_path = os.path.join(MEDIA_ROOT, 'article', file_name)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    url = f"{request.scheme}://{request.get_host()}{reverse('media', kwargs={'path': 'article'})}/{file_name}"
    return Response({"location": url})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def upload_img(request):
    """
    element组件上传图片接口
    :param request:
    :return:
    """
    return Response({'status': '1', 'msg': 'ok'})


@api_view(['GET'])
def index_data(request):
    """
    获取过去七天的文章、动态数据量
    """
    current_time = timezone.now()
    past_time = current_time - datetime.timedelta(days=7)
    article_count = Article.objects.filter(Q(create_time__gte=past_time) & Q(create_time__lte=current_time),
                                           is_delete=False).count()
    message_count = Message.objects.filter(Q(create_time__gte=past_time) & Q(create_time__lte=current_time),
                                           is_delete=False).count()
    return_data = {
        'article_count': article_count,
        'message_count': message_count
    }
    return APIResponse(1, 'ok', return_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wang_editor_upload_img(request):
    """
    wangeditor富文本编辑器图片上传接口
    :param request:
    :return: "errno": 0,
            "data": [
                "图片1地址",
                "图片2地址",
                "……"
            ]
    """
    data = request.data
    file = data.get('file')
    file_suffix = file.name.split('.')[-1]
    file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_suffix
    directory = os.path.join(MEDIA_ROOT, 'article')
    if not os.path.exists(directory):
        os.mkdir(directory)
    file_path = os.path.join(MEDIA_ROOT, 'article', file_name)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    url = f"{request.scheme}://{request.get_host()}{reverse('media', kwargs={'path': 'article'})}/{file_name}"
    return Response({'errno': 0, 'data': url})

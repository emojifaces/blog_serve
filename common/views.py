import os
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid
from myblog_serve.settings import MEDIA_ROOT, MEDIA_URL


@api_view(['POST'])
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
def upload_img(request):
    data = request.data
    print(data)

    return Response({'code': 1})

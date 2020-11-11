from django.db import models
from common.models import Common
from user.models import User


class Message(Common):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='message_user')  # 用户
    content = models.TextField(null=True, blank=True)  # 内容

    class Meta:
        db_table = 'message'


class MessageImg(models.Model):
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING, related_name='img_message')  # 动态
    img = models.ImageField(upload_to='message')  # 图片

    class Meta:
        db_table = 'message_img'

from django.db import models
from datetime import datetime


class Common(models.Model):
    is_delete = models.BooleanField(default=False)  # 是否删除
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间

    class Meta:
        abstract = True

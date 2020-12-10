from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    sex_type = (
        (0, '女'),
        (1, '男'),
        (2, '未知')
    )
    nickname = models.CharField(max_length=20, null=True)  # 昵称
    user_head = models.ImageField(upload_to='head')  # 用户头像
    phone_number = models.CharField(max_length=20, null=True)  # 手机号码
    weibo = models.CharField(max_length=20, null=True)  # 微博昵称
    profile = models.CharField(max_length=50, null=True)  # 个人简介
    sex = models.SmallIntegerField(choices=sex_type, default=2)  # 性别

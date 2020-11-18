from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=20, null=True)  # 昵称
    user_head = models.ImageField(upload_to='head')  # 用户头像
    phone_number = models.CharField(max_length=20, null=True)  # 手机号码
    weibo = models.CharField(max_length=20, null=True)  # 微博昵称
    profile = models.CharField(max_length=50, null=True)  # 个人简介

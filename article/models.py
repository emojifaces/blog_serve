from django.db import models
from common.models import Common
from user.models import User
class Article(Common):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='articles')
    title = models.CharField(max_length=255,null=True,blank=True)  # 标题
    content = models.TextField(null=True,blank=True)   # 内容

    class Meta:
        db_table = 'article'
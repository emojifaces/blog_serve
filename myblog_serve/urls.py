from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework import routers
from article.views import ArticleViewSet
from user.views import UserViewSet

router = routers.SimpleRouter()

router.register('article', ArticleViewSet)
router.register('user',UserViewSet)

urlpatterns = [
    path('media', serve, {'document_root': settings.MEDIA_ROOT})
]
urlpatterns += router.urls
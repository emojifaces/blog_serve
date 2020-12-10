from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from rest_framework import routers
from article.views import ArticleViewSet
from user.views import UserViewSet, MyTokenObtainPairView
from message.views import MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from common.views import *

router = routers.SimpleRouter()

router.register('api/article', ArticleViewSet)
router.register('api/user', UserViewSet)
router.register('api/message', MessageViewSet)

urlpatterns = [
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/article_upload_img', article_upload_img),
    path('api/upload_img', upload_img),
    path('api/index_data', index_data),
    path('api/wangEditor_uploadImg', wang_editor_upload_img),
]

urlpatterns += router.urls

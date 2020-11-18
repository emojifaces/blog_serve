from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from rest_framework import routers
from article.views import ArticleViewSet
from user.views import UserViewSet
from message.views import MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from common.views import upload_img

router = routers.SimpleRouter()

router.register('article', ArticleViewSet)
router.register('user', UserViewSet)
router.register('message', MessageViewSet)

urlpatterns = [
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload_img', upload_img),
]

urlpatterns += router.urls

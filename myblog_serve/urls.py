from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from rest_framework import routers
from article.views import ArticleViewSet
from user.views import UserViewSet
from message.views import MessageViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.SimpleRouter()

router.register('article', ArticleViewSet)
router.register('user', UserViewSet)
router.register('message', MessageViewSet)

urlpatterns = [
    path('media', serve, {'document_root': settings.MEDIA_ROOT}),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls

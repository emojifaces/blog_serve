from django.urls import path
from .views import *


urlpatterns = [
    path('test1',Test1.as_view()),
    path('test2',Test2.as_view()),
]
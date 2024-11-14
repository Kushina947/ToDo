from django.urls import path
from .views import *

app_name = 'thread'
urlpatterns = [
    path('<int:pk>/', ThreadView.as_view(), name='thread'),
    path('create/<str:code>/', ThreadCreateView.as_view(), name='create'),
]
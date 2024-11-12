from django.urls import path
from .views import *

app_name = 'lecture'
urlpatterns = [
    path('<str:pk>/', LectureView.as_view(), name='lecture'),
]
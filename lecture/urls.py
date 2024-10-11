from django.urls import path
from .views import *

app_name = 'base'

urlpatterns = [
    path('', LectureView.as_view(), name='home'),
]
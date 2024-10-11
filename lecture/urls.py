from django.urls import path
from .views import *

urlpatterns = [
    path('lecture/', LectureView.as_view(), name='home'),
    path('lecture/register/', Lecture_addView.as_view(), name='lecture_add'),
]
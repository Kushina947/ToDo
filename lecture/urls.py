from django.urls import path
from .views import *

urlpatterns = [
    path('', LectureView.as_view(), name='lecture'),
    path('register/', Lecture_addView.as_view(), name='lecture_add'),
]
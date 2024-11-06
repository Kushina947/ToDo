from django.urls import path
from .views import *

urlpatterns = [
    path('', LectureView.as_view(), name='lecture_list'),
    path('add', Lecture_addView.as_view(), name='add'),
    path('register/', Lecture_addView.as_view(), name='lecture_add'),
]
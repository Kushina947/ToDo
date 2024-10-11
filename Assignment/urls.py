from django.urls import path
from .views import *


urlpatterns = [
    path('assignment/', AssignmentView.as_view(), name='assignment'),
    path('assignment/register/', Assignment_addView.as_view(), name='assignment_add')
]
from django.urls import path
from .views import *


urlpatterns = [
    path('', AssignmentView.as_view(), name='assignment'),
    path('register/', Assignment_addView.as_view(), name='assignment_add')
]
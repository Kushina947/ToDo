from django.urls import path
from .views import *


urlpatterns = [
    path('', ThreadView.as_view(), name='view'),
]
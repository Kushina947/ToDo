from django.urls import path
from .views import *


urlpatterns = [
    path('', LoginView.as_view(), name='view'),
    path('register', SignUpView.as_view(), name='register'),
]
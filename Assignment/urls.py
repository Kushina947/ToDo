from django.urls import path
from .views import *

app_name = 'assignment'
urlpatterns = [
    path('create/<str:code>/', AssignmentCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', AssignmentDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', AssignmentUpdateView.as_view(), name='edit'),
    path('<int:pk>/', AssignmentDetailView.as_view(), name='detail'),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/users/<int:userId>/', UserDetailView.as_view(), name='user-detail')
]

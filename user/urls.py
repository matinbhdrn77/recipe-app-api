"""
Urls for handling user registration and login
"""
from django.urls import path, include

from .views import CreateUserView, CreateTokenView

app_name = 'user'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
]

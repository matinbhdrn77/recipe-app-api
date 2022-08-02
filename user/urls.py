"""
Urls for handling user registration and login
"""
from django.urls import path, include

from .views import CreateUserView

app_name = 'user'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
]

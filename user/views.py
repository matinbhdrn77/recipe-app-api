"""
API class base view for handling user features
"""
from rest_framework import generics

from .serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """"Create a new user in the system"""
    serializer_class = UserSerializer
    
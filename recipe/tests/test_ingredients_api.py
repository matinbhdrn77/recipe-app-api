"""
Tests for ingredinets api.
"""
import email
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(**params):
    """Create and return a user."""
    return get_user_model().objects.create_user(**params)


class PublicIngreeintApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_requiered(self):
        """Test auth is required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    

class PrivateIngredientsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retirieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        ing1 = Ingredient.objects.create(user=self.user, name='ingredient1')
        ing2 = Ingredient.objects.create(user=self.user, name='ingredient2')

        res = self.client.get(INGREDIENTS_URL)

        Ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(Ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""
        user2 = create_user(email='user2@ex.com')
        Ingredient.objects.create(user= user2, name='ingredient3')
        ingredient = Ingredient.objects.create(user=self.user, name='ingredient4')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0].name, ingredient.name)
        self.assertEqual(res.data[0].id, ingredient.id)  
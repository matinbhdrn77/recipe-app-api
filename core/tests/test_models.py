from tkinter.messagebox import NO
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="email@test.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_succesful(self):
        email = 'test@ex.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new user"""
        sample_emails = [
            ['test1@EX.com', 'test1@ex.com'],
            ['Test2@Ex.com', 'Test2@ex.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'pass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating user without an email address raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_create_superuser(self):
        """Test creating superuser."""
        user = get_user_model().objects.create_superuser(
            'test@ex.com',
            'pass123,'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is succesful."""
        user = get_user_model().objects.create_user(
            'test@ex.com',
            'pass123,'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='title test',
            time_minutes=5,
            price=Decimal('5.50'),
            description='description test',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="tagtest")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredinet(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)
    
    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
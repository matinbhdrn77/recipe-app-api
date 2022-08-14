"""
Tests for tags API.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


def create_user(email="test@email.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_uesr(email, password)

def create_tag(user, name):
    """Create and return a new tag."""
    return Tag.objects.create(user, name)

class PublicTagsAPITests(TestCase):
    """Test public tag features."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for all APIs."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test private tag features."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate()

    def test_retireve__tags(self):
        """Test retirieving a list of tags."""
        create_tag(self.user, 'tag1')
        create_tag(self.user, 'tag2')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
    
    def test_tags_limited_to_user(self):
        """Test list of tags is limited to user"""
        another_user = create_user(email='another@ex.com', password='testes123')
        create_tag(another_user, 'tag3')
        tag = create_tag(self.user, 'tag4')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)


    


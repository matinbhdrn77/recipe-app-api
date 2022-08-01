"""
Test for Django admin modidfication
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Test for Django admin."""

    def setUp(self):
        """Create user and clien"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@ex.com',
            password='test123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='ueser@ex.com',
            password='pass123',
            name='Test User'
        )
     
    def test_user_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edite_user_page(self):
        """Test the edite user page work"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

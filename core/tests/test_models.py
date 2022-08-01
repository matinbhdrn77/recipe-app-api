from django.test import TestCase
from django.contrib.auth import get_user_model


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
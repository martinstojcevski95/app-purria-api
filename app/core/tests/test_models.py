"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['test3@example.COM', 'test3@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Creating user without email raises ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test for creating superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_contract(self):
        """Test creating a contract is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        contract = models.Contract.objects.create(
            user=user,
            name='Simple contract name',
            description='Simple contract description',
            level=100
        )

        self.assertEqual(str(contract), contract.name)
        self.assertEqual(contract.user, user)

    def test_create_garden(self):
        """Test creating garden is successful."""
        user = create_user()
        garden = models.Garden.objects.create(user=user,
                                              name='garden', level=1)

        self.assertEqual(str(garden), garden.name)

    def test_create_plant(self):
        """Test creating plant is successful."""
        user = create_user()
        plant = models.Plant.objects.create(
            garden_id="123-123-123",
            user=user,
            name="plant",
        )

        self.assertEqual(str(plant), plant.name)
        self.assertEqual(len(models.Plant.objects.all()), 1)

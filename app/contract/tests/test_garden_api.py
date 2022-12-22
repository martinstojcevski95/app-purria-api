"""
Tests for the garden APIs.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Garden

from contract.serializers import GardenSerializer


GARDENS_URL = reverse('contract:garden-list')


def detail_url(garden_id):
    """Create and return garden detail url."""
    return reverse('contract:garden-detail', args=[garden_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email, password)


class PublicGardensApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving gardens."""
        response = self.client.get(GARDENS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGardensApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_gardens(self):
        """Test retrieving list of gardens."""
        Garden.objects.create(user=self.user,
                              name='test', level=1)
        Garden.objects.create(user=self.user,
                              name='test123', level=2)

        response = self.client.get(GARDENS_URL)

        gardens = Garden.objects.all().order_by('-name')
        serializer = GardenSerializer(gardens, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_garden(self):
        """Test updating garden."""
        garden = Garden.objects.create(user=self.user, name='garden name')

        payload = {'name': 'new garden name'}

        url = detail_url(garden.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        garden.refresh_from_db()
        self.assertEqual(garden.name, payload['name'])

    def test_delete_gardens(self):
        """Test deleting garden."""
        garden = Garden.objects.create(user=self.user, name='Contract_Name')

        url = detail_url(garden.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        gardens = Garden.objects.filter(user=self.user)
        self.assertFalse(gardens.exists())

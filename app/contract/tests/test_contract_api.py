"""
Test for contract APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Contract

from contract.serializers import (
    ContractSerializer,
    ContractDetailSerializer,
)

CONTRACTS_URL = reverse('contract:contract-list')

def detail_url(contract_id):
    """Create and return contract detail URL."""
    return reverse('contract:contract-detail', args=[contract_id])

def create_contract(user, **params):
    """Create and return simple contract."""
    defaults = {
        'name': "contract name",
        'description': 'contract description',
        'level': 1,
    }
    defaults.update(params)

    contract = Contract.objects.create(user=user, **defaults)
    return contract

def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)


class PublicContractAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        response = self.client.get(CONTRACTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateContractAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='testpass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_contracts(self):
        """Test retrieving list of contracts"""
        create_contract(user=self.user)
        create_contract(user=self.user)

        response = self.client.get(CONTRACTS_URL)

        contracts = Contract.objects.all().order_by('-id')
        serializer = ContractSerializer(contracts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_contract_list_limited_to_user(self):
        """Test list of contracts is limited to authenticated user only."""
        other_user = create_user(email='other@example.com',
            password='password123',
        )
        create_contract(user=other_user)
        create_contract(user=self.user)

        response = self.client.get(CONTRACTS_URL)

        contracts = Contract.objects.filter(user=self.user)
        serializer = ContractSerializer(contracts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_contract_detail(self):
        """Test get contract detail."""
        contract = create_contract(user=self.user)

        url = detail_url(contract.id)
        response = self.client.get(url)

        serializer = ContractDetailSerializer(contract)

        self.assertEqual(response.data, serializer.data)
        self.assertIn('description', serializer.data)

    def test_create_contract(self):
        """Test creating contract."""
        payload = {
            'name': 'new contract',
            'level': 1,
        }
        response = self.client.post(CONTRACTS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=response.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(contract, k), v)
        self.assertEqual(contract.user, self.user)

    def test_partial_update_not_allowed(self):

        contract = create_contract(
            user=self.user,
            name='contract name',
            level=1
        )
        url = detail_url(contract.id)
        payload = {'name': 'updated contract name'}
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotEqual(contract.name, payload['name'])

    def test_delete_contract(self):
        """Test deleting contract successful."""
        contract = create_contract(user=self.user)

        url = detail_url(contract.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contract.objects.filter(id=contract.id).exists())

    def test_delete_other_user_contract_error(self):
        """Test trying to delete another user contract gives error."""
        new_user = create_user(email='user2@example.com', password='pas123')
        contract = create_contract(user=new_user)

        url = detail_url(contract.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Contract.objects.filter(id=contract.id).exists())
"""
Views for the contract APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Contract
from contract import serializers


class ContractViewSet(viewsets.ModelViewSet):
    """View for manage contract APIs."""
    serializer_class = serializers.ContractDetailSerializer
    queryset = Contract.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'list', 'delete']

    def get_queryset(self):
        """Retrieve contracts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ContractSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new contract."""
        serializer.save(user=self.request.user)

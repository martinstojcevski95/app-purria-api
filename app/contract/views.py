"""
Views for the contract APIs.
"""
from rest_framework import (
    viewsets,
    mixins,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    Contract,
    Garden,
    Plant,
)

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.ContractSerializer(queryset, many=True)
        response = {
            "result": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)


class GardenViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Manage gardens in the database."""
    serializer_class = serializers.GardenSerializer
    queryset = Garden.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(
            user=self.request.user).order_by('-name')
        garden_by_contract_name = self.request.query_params.get("name")
        if garden_by_contract_name is not None:
            queryset = queryset.filter(
                name__icontains=garden_by_contract_name).values()
        return queryset


class PlantViewSet(mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Manage plants in the database."""
    serializer_class = serializers.PlantSerializer
    queryset = Plant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

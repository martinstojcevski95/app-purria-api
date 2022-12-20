"""
Serializers for contract APIs.
"""
from rest_framework import serializers
from core.models import Contract


class ContractSerializer(serializers.ModelSerializer):
    """Serializer for contracts."""

    id = serializers.CharField(read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'name', 'level']
        read_only_fields = ['id']


class ContractDetailSerializer(ContractSerializer):
    """Serializer for contract detail view."""

    class Meta(ContractSerializer.Meta):
        fields = ContractSerializer.Meta.fields + ['description']

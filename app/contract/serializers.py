"""
Serializers for contract APIs.
"""
from rest_framework import serializers
from core.models import (
    Contract,
    Garden,
    Plant,
)


class PlantSerializer(serializers.ModelSerializer):
    """Serializer for plants."""

    class Meta:
        model = Plant
        fields = ['id', 'garden_id', 'name']


class GardenSerializer(serializers.ModelSerializer):
    """Serialier for gardens."""

    plants = PlantSerializer(many=True, required=False)

    class Meta:
        model = Garden
        fields = ['id', 'name', 'level', 'plants']
        read_only_fields = ['id']


class ContractSerializer(serializers.ModelSerializer):
    """Serializer for contracts."""

    id = serializers.CharField(read_only=True)
    gardens = GardenSerializer(many=True, required=False)

    class Meta:
        model = Contract
        fields = ['id', 'name', 'level', 'gardens']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create contract."""
        contract = Contract.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for level in range(contract.level * 10):
            garden = Garden.objects.create(user=auth_user,
                                           name=contract.name,
                                           level=contract.level)
            for i in range(garden.level * 10):
                plant = Plant.objects.create(
                    garden_id=garden.id,
                    user=garden.user,
                    name='newplant',
                )
                garden.plants.add(plant)

            contract.gardens.add(garden)

        return contract

    def validate(self, attrs):
        """Validate if contract already exist."""
        if self.context['request'].method == 'POST':
            current_user_email = self.context['request'].user.email
            check_contract_user = Contract.objects.filter(
                user__email=current_user_email).filter(
                    name=attrs['name'].lower()).exists()
            if check_contract_user:
                raise serializers.ValidationError(
                    'contract with name already exists')
            return attrs
        return super().validate(attrs)


class ContractDetailSerializer(ContractSerializer):
    """Serializer for contract detail view."""

    class Meta(ContractSerializer.Meta):
        fields = ContractSerializer.Meta.fields + ['description']

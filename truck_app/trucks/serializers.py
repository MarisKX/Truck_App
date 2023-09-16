"""
Serializers for the trucks API View
"""
from rest_framework import serializers
from trucks.models import Truck


class TruckSerializer(serializers.ModelSerializer):
    """Serializer for trucks"""

    class Meta:
        model = Truck
        fields = [
            'id',
            'last_edit_by',
            'licence_plate',
            'make',
            'model',
            'year',
            'vin',
        ]
        read_only_fields = ['id', 'last_edited_by', ]


class TruckDetailSerializer(TruckSerializer):
    """Serializer for recipe detail view"""

    class Meta(TruckSerializer.Meta):
        fields = TruckSerializer.Meta.fields + ['color', 'engine', ]

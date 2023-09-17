"""
Serializers for the maintenance and jobs API View
"""
from rest_framework import serializers
from .models import MaintenanceGroup


class MaintenanceGroupSerializer(serializers.ModelSerializer):
    """Serializer for Maintenance Groups"""

    class Meta:
        model = MaintenanceGroup
        fields = ['id', 'name', 'display_name', ]
        read_only_fields = ['id', 'name', ]


class MaintenanceGroupDetailSerializer(MaintenanceGroupSerializer):
    """Serializer for Maintenance Groups Details"""

    class Meta(MaintenanceGroupSerializer.Meta):
        fields = MaintenanceGroupSerializer.Meta.fields + ['code', ]

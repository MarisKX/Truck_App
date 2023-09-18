"""
Serializers for the maintenance and jobs API View
"""
from rest_framework import serializers
from .models import MaintenanceGroup, Job


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobs"""
    class Meta:
        model = Job
        fields = ['id', 'name', 'display_name', ]
        read_only_fields = ['id', 'name', ]


class MaintenanceGroupSerializer(serializers.ModelSerializer):
    """Serializer for Maintenance Groups"""
    jobs = JobSerializer(many=True, required=False)

    class Meta:
        model = MaintenanceGroup
        fields = ['id', 'name', 'display_name', 'jobs', ]
        read_only_fields = ['id', 'name', ]

    def create(self, validated_data):
        """Create a Maintenance Group"""
        jobs = validated_data.pop('jobs', [])
        maintenance_group = MaintenanceGroup.objects.create(**validated_data)

        for job in jobs:
            job_obj, created = Job.objects.get_or_create(
                **job
            )
            maintenance_group.jobs.add(job_obj)

        return maintenance_group


class MaintenanceGroupDetailSerializer(MaintenanceGroupSerializer):
    """Serializer for Maintenance Groups Details"""

    class Meta(MaintenanceGroupSerializer.Meta):
        fields = MaintenanceGroupSerializer.Meta.fields + ['code', ]

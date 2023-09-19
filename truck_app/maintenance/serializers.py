"""
Serializers for the maintenance and jobs API View
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import MaintenanceGroup, Job, Category


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobs"""
    class Meta:
        model = Job
        fields = ['id', 'name', 'display_name', ]
        read_only_fields = ['id', 'name', ]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for jobs"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name', ]
        read_only_fields = ['id', 'name', ]


class MaintenanceGroupSerializer(serializers.ModelSerializer):
    """Serializer for Maintenance Groups"""
    jobs = JobSerializer(many=True, required=False)

    class Meta:
        model = MaintenanceGroup
        fields = ['id', 'category', 'name', 'display_name', 'jobs', ]
        read_only_fields = ['id', 'name', ]

    def _get_or_create_jobs(self, jobs, maintenance_group):
        """Handle getting or creating jobs as needed"""
        for job in jobs:
            job_obj, created = Job.objects.get_or_create(
                **job
            )
            maintenance_group.jobs.add(job_obj)

    def create(self, validated_data):
        """Create a Maintenance Group"""
        jobs = validated_data.pop('jobs', [])
        if not jobs:
            raise ValidationError(
                {'jobs': 'At least one job must be provided.'})
        maintenance_group = MaintenanceGroup.objects.create(**validated_data)
        self._get_or_create_jobs(jobs, maintenance_group)

        return maintenance_group

    def update(self, instance, validated_data):
        """Update a Maintenance Group"""
        jobs = validated_data.pop('jobs', None)
        if jobs is not None:
            if not jobs:
                raise ValidationError(
                    {'jobs': 'At least one job must be provided.'})
            instance.jobs.clear()
            self._get_or_create_jobs(jobs, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MaintenanceGroupDetailSerializer(MaintenanceGroupSerializer):
    """Serializer for Maintenance Groups Details"""

    class Meta(MaintenanceGroupSerializer.Meta):
        fields = MaintenanceGroupSerializer.Meta.fields + ['code', ]

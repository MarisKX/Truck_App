"""
Serializers for the maintenance and jobs API View
"""
from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from .models import MaintenanceGroup, Job


class JobSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Job
        fields = ('id', 'name', 'display_name')
        read_only_fields = ['id', 'name', ]


class MaintenanceGroupSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, required=True)

    class Meta:
        model = MaintenanceGroup
        fields = ('id', 'code', 'name', 'display_name', 'jobs')
        read_only_fields = ['id', 'name', ]

    def _get_or_create_jobs(self, jobs_data):
        """Handle getting or creating jobs as needed"""
        job_instances = []
        for job in jobs_data:
            display_name = job.get('display_name')
            print(f"Checking for job with display_name={display_name}")
            try:
                job_obj, created = Job.objects.get_or_create(display_name=display_name)
                print(f"Job with display_name={display_name} {'created' if created else 'already exists'}")
                job_instances.append(job_obj)
            except Exception as e:
                print(f"Error while trying to get or create job with display_name={display_name}: {str(e)}")
                raise serializers.ValidationError(f"Failed to get or create job with display name {display_name}: {str(e)}")
        return job_instances

    def create(self, validated_data):
        """Create a maintenance code"""

        jobs_data = validated_data.pop('jobs', [])
        for job in jobs_data:
            print(job)

        if not jobs_data:  # Check if jobs_data is empty
            raise serializers.ValidationError("Maintenance code must have at least one job")

        with transaction.atomic():
            # Validate or create job instances
            job_instances = self._get_or_create_jobs(jobs_data)
            for job in job_instances:
                print(job.name)

            # Now create the MaintenanceCode instance with the validated jobs
            maintenance_code = MaintenanceCode.objects.create(**validated_data)
            print(f"Maintenance Code saved as: " + maintenance_code.name + "!")

            # Link the job instances with the maintenance code
            maintenance_code.jobs.set(job_instances)

        return maintenance_code

    def update(self, instance, validated_data):
        """Update recipe"""
        jobs = validated_data.pop('jobs', None)
        if jobs is not None:
            instance.jobs.clear()
            self._get_or_create_jobs(jobs, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

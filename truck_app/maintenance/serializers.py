"""
Serializers for the maintenance and jobs API View
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import MaintenanceCode, Job


class JobSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Job
        fields = ('id', 'name', 'display_name')


class MaintenanceCodeSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = MaintenanceCode
        fields = ('id', 'code', 'name', 'display_name', 'jobs')

    def validate_jobs(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("At least one job is required.")
        return value

    def create(self, validated_data):
        jobs_data = validated_data.pop('jobs')
        job_instances = []
        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                display_name=job_data['display_name'],
                defaults={
                    'name': job_data.get(
                        'name', job_data[
                            'display_name'].replace(" ", "_").lower())}
            )
            if not created and job.name != job_data.get('name', job.name):
                raise ValidationError(
                    f"Job with display_name {job_data['display_name']} already exists with a different name.")  # noqa
            job_instances.append(job)

        maintenance_code = MaintenanceCode.objects.create(**validated_data)
        maintenance_code.jobs.set(job_instances)
        return maintenance_code

    def update(self, instance, validated_data):
        jobs_data = validated_data.pop('jobs')

        # Update the MaintenanceCode instance
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.display_name = validated_data.get(
            'display_name', instance.display_name
        )
        instance.save()

        # Update or create Job instances
        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                maintenance_code=instance, **job_data
            )
            if not created:
                job.name = job_data.get('name', job.name)
                job.display_name = job_data.get(
                    'display_name', job.display_name
                )
                job.save()

        return instance

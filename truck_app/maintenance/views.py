"""
Views for Maintenance Groups
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from maintenance.models import MaintenanceGroup, Job
from maintenance import serializers


class MaintenanceGroupViewSet(viewsets.ModelViewSet):
    """Manage Maintenance Codes in the database"""
    serializer_class = serializers.MaintenanceGroupDetailSerializer
    queryset = MaintenanceGroup.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve all maintenance groups, ordered by name"""
        return self.queryset.all().order_by('name')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.MaintenanceGroupSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Maintenance group"""
        serializer.save()

    def update(self, request, *args, **kwargs):
        # Enforce that `jobs` should not be empty if method is PUT
        if request.method == 'PUT':
            if 'jobs' not in request.data or not request.data['jobs']:
                return Response(
                    {'jobs': 'This field is required.'},
                    status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class JobViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Manage Jobs in the database"""
    serializer_class = serializers.JobSerializer
    queryset = Job.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve all jobs, ordered by name"""
        return self.queryset.all().order_by('name')

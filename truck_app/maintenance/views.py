from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from maintenance.models import MaintenanceCode, Job
from maintenance import serializers


class JobViewSet(viewsets.ModelViewSet):
    """Manage Jobs in the database"""
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class MaintenanceCodeViewSet(viewsets.ModelViewSet):
    """Manage Maintenance Codes in the database"""
    queryset = MaintenanceCode.objects.all()
    serializer_class = serializers.MaintenanceCodeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.MaintenanceCodeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

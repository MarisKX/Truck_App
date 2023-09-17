from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from maintenance.models import MaintenanceGroup, Job
from maintenance import serializers


class JobViewSet(viewsets.ModelViewSet):
    """Manage Jobs in the database"""
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Data of jobs before validation: {serializer.initial_data}")
        is_valid = serializer.is_valid()
        print(f"Is serializer valid: {is_valid}")
        if is_valid:
            serializer.save()
        else:
            print(f"Serializer errors: {serializer.errors}")

    def perform_update(self, serializer):
        serializer.save()


class MaintenanceGroupViewSet(viewsets.ModelViewSet):
    """Manage Maintenance Codes in the database"""
    queryset = MaintenanceGroup.objects.all()
    serializer_class = serializers.MaintenanceGroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve all maintenance groups, ordered by name"""
        return self.queryset.all().order_by('name')

    def _params_to_int(self, qs):
        """Convert a list of strings to integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.MaintenanceGroupSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        print(f"Data of maintencecode before validation: {serializer.initial_data}")
        is_valid = serializer.is_valid()
        print(f"Is serializer valid: {is_valid}")
        if is_valid:
            serializer.save()
        else:
            print(f"Serializer errors: {serializer.errors}")

    def perform_update(self, serializer):
        serializer.save()

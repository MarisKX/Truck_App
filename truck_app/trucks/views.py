"""
Views for the trucks API's
"""
from rest_framework import (
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from trucks.models import (
    Truck,
)
from trucks import serializers


class TruckViewSet(viewsets.ModelViewSet):
    """View for manage trucks API's"""
    serializer_class = serializers.TruckDetailSerializer
    queryset = Truck.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.TruckSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

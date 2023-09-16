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
    serializer_class = serializers.TruckSerializer
    queryset = Truck.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
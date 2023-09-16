
"""
Tests for Trucks APis
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from trucks.models import Truck
from trucks.serializers import TruckSerializer


TRUCKS_URL = reverse('trucks:truck-list')

def create_truck(user, **params):
    """Create and return a sample truck"""
    defaults = {
        'licence_plate': "AH6814",
        'make': "FREIGHTLINER",
        'model': "CASCADIA 125",
        'year': "2016",
    }
    defaults.update(params)

    truck = Truck.objects.create(last_edit_by=user, **defaults)
    return truck

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicTruckApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(TRUCKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTruckApiTests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_trucks(self):
        """Test retrieving a list of trucks"""
        create_truck(
            user=self.user,
            vin="3AKJGLD58GSHR6402"
        )
        create_truck(
            user=self.user,
            vin="3AKJGLD58GSHR6403"
        )

        res = self.client.get(TRUCKS_URL)

        trucks = Truck.objects.all().order_by('id')
        serializer = TruckSerializer(trucks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

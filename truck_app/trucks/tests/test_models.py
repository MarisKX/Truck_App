"""
Tests for models.
"""
from decimal import Decimal  # noqa
from django.test import TestCase
from django.contrib.auth import get_user_model

from trucks.models import Truck


def create_user(email='user@example.com', password='Pass1234'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_truck(self):
        """Test creating a truck is successfull"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        truck = Truck.objects.create(
            last_edit=user,
            licence_plate="AH6814",
            make="FREIGHTLINER",
            model="CASCADIA 125",
            year="2016",
            vin="3AKJGLD58GSHR6402"
        )

        self.assertEqual(str(truck), truck.licence_plate)

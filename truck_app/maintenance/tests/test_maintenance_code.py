"""
Tests for maintenance codes and jobs API
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from maintenance.models import MaintenanceCode
from maintenance.serializers import (
    MaintenanceCodeSerializer,
)


MAINTENANCE_URL = reverse('maintenance:maintenancecode-list')
JOB_URL = reverse('maintenance:job-list')


def detail_url_maintenance(maintenance_id):
    """Create and return a MaintenanceCode detail URL"""
    return reverse('maintenance:maintenancecode-detail', args=[maintenance_id])


def detail_url_job(job_id):
    """Create and return a Job detail URL"""
    return reverse('maintenance:job-detail', args=[job_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicMaintenanceApiTests(TestCase):
    """Test unauthenticated API requests for Maintenance"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to retrieve MaintenanceCode"""
        res = self.client.get(MAINTENANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.get(JOB_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMaintenanceApiTests(TestCase):
    """Test authenticated API requests for Maintenance"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass1235')
        self.client.force_authenticate(self.user)

    def test_retrieve_maintenance_codes(self):
        """Test retrieving a list of Maintenance Codes"""

        MaintenanceCode.objects.create(
            code="A+",
            display_name="Maintenance A+"
        )
        MaintenanceCode.objects.create(
            code="B-",
            display_name="Maintenance B-"
        )

        res = self.client.get(MAINTENANCE_URL)
        codes = MaintenanceCode.objects.all().order_by('id')
        serializer = MaintenanceCodeSerializer(codes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_maintenance_code(self):
        """Test creating a Maintenance Code"""
        payload = {
            'code': 'A+',
            'display_name': 'Maintenance A+',
            'jobs': [
                {'name': 'Job1', 'display_name': 'Job Display 1'},
                {'name': 'Job2', 'display_name': 'Job Display 2'}
            ]
        }
        res = self.client.post(MAINTENANCE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_maintenance_code_no_jobs(self):
        """Test creating a Maintenance Code with no jobs should fail"""
        payload = {
            'code': 'A++',
            'display_name': 'Maintenance A++',
            'jobs': []
        }
        res = self.client.post(MAINTENANCE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

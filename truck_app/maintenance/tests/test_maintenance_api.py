"""
Tests for maintenance groups API
"""
# Django general imports
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
# Rest Framework imports
from rest_framework import status
from rest_framework.test import APIClient
# Custom imports
from maintenance.models import MaintenanceGroup, Job
from maintenance.serializers import (
    MaintenanceGroupSerializer,
    MaintenanceGroupDetailSerializer,
)


MAINTENANCE_URL = reverse('maintenance:maintenancegroup-list')


def detail_url(maintenancegroup_id):
    """Create and return a maintenance group detail url"""
    return reverse(
        'maintenance:maintenancegroup-detail',
        args=[maintenancegroup_id],
    )


def create_maintenance_group(**params):
    """Create and return a sample maintenance group"""
    defaults = {
        'code': 'A',
        'display_name': 'Maintenance A',
    }
    defaults.update(params)
    maintenance_group = MaintenanceGroup.objects.create(**defaults)
    return maintenance_group


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


class PrivateMaintenanceApiTests(TestCase):
    """Test authenticated API requests for Maintenance"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='pass1235')
        self.client.force_authenticate(self.user)

    def test_retrieve_maintenance_groups(self):
        """Test retrieving a list of Maintenance Groups"""

        MaintenanceGroup.objects.create(
            code="A+",
            display_name="Maintenance A+"
        )
        MaintenanceGroup.objects.create(
            code="B-",
            display_name="Maintenance B-"
        )

        res = self.client.get(MAINTENANCE_URL)
        groups = MaintenanceGroup.objects.all().order_by('name')
        serializer = MaintenanceGroupSerializer(groups, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_maintenance_group_details(self):
        """Test get maintenance group details"""
        maintenance_group = create_maintenance_group()

        url = detail_url(maintenance_group.id)
        res = self.client.get(url)

        serializer = MaintenanceGroupDetailSerializer(maintenance_group)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_maintenance_group(self):
        """Test creating a maintenance group"""
        payload = {
            'code': 'B',
            'display_name': 'Maintenance B',
            'jobs': [
                {'display_name': 'Oil Change'},
            ]
        }
        res = self.client.post(MAINTENANCE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        maintenance_group = MaintenanceGroup.objects.get(id=res.data['id'])

        for k, v in payload.items():
            if k == 'jobs':
                jobs = maintenance_group.jobs.all()
                job_list = []
                for job in jobs:
                    job_list.append({'display_name': job.display_name})
                self.assertEqual(job_list, v)
            else:
                self.assertEqual(getattr(maintenance_group, k), v)

    def test_create_maintenance_group_with_empty_fields_fails(self):
        """Test that creating a maintenance group with empty fields fails"""

        payload = {'code': '', 'display_name': 'Maintenance B'}
        res = self.client.post(MAINTENANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'code': 'B', 'display_name': ''}
        res = self.client.post(MAINTENANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'code': '', 'display_name': ''}
        res = self.client.post(MAINTENANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_maintenance_group(self):
        """
        Test updating a maintenance group with patch,
        including automatic name update
        """

        maintenance_group = MaintenanceGroup.objects.create(
            code="A",
            display_name="Maintenance A"
        )

        self.assertEqual(maintenance_group.name, "maintenance_a")

        url = detail_url(maintenance_group.id)

        payload = {'code': 'A1'}
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        maintenance_group.refresh_from_db()
        self.assertEqual(maintenance_group.code, payload['code'])
        self.assertEqual(maintenance_group.display_name, "Maintenance A")
        self.assertEqual(maintenance_group.name, "maintenance_a")

        payload = {'display_name': 'Maintenance A1'}
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        maintenance_group.refresh_from_db()
        self.assertEqual(
            maintenance_group.display_name,
            payload['display_name'],
        )
        self.assertEqual(maintenance_group.code, 'A1')
        self.assertEqual(maintenance_group.name, "maintenance_a1")

    def test_full_update_maintenance_group(self):
        """Test updating a maintenance group with put"""

        maintenance_group = MaintenanceGroup.objects.create(
            code="A",
            display_name="Maintenance A"
        )

        url = detail_url(maintenance_group.id)
        payload = {
            'code': 'A1',
            'display_name': 'Maintenance A1',
            'jobs': [{'display_name': 'Brake Disc Change'}]}

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        maintenance_group.refresh_from_db()
        self.assertEqual(maintenance_group.code, payload['code'])
        self.assertEqual(
            maintenance_group.display_name,
            payload['display_name'],
        )
        self.assertEqual(maintenance_group.name, "maintenance_a1")

    def test_create_maintenance_group_with_new_jobs(self):
        """Test creating a maintenance group with new job"""
        payload = {
            'code': 'A',
            'display_name': 'Maintenance A',
            'jobs': [
                {'display_name': 'Oil Change'},
                {'display_name': 'Oil Filter Change'},
            ]
        }
        res = self.client.post(MAINTENANCE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        maintenance_groups = MaintenanceGroup.objects.all()
        self.assertEqual(maintenance_groups.count(), 1)
        maintenance_group = maintenance_groups[0]
        self.assertEqual(maintenance_group.jobs.count(), 2)
        for job in payload['jobs']:
            exists = maintenance_group.jobs.filter(
                display_name=job['display_name']
            ).exists()
            self.assertTrue(exists)

    def test_create_maintenance_group_with_existing_jobs(self):
        """Test creating a maintenance group with existing job"""
        job_1 = Job.objects.create(display_name='Air Filter Change')
        payload = {
            'code': 'A+',
            'display_name': 'Maintenance A+',
            'jobs': [
                {'display_name': 'Air Filter Change'},
                {'display_name': 'Oil Filter Change'},
            ]
        }

        res = self.client.post(MAINTENANCE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        maintenance_groups = MaintenanceGroup.objects.all()
        self.assertEqual(maintenance_groups.count(), 1)
        maintenance_group = maintenance_groups[0]
        self.assertEqual(maintenance_group.jobs.count(), 2)
        self.assertIn(job_1, maintenance_group.jobs.all())
        for job in payload['jobs']:
            exists = maintenance_group.jobs.filter(
                display_name=job['display_name']
            ).exists()
            self.assertTrue(exists)

    def test_create_job_on_update(self):
        """Test creating a job when update maintenance group"""
        maintenance_group = MaintenanceGroup.objects.create(
            code="Custom1",
            display_name="Custom1"
        )
        payload = {'jobs': [{'display_name': 'Brake Pad Change'}]}
        url = detail_url(maintenance_group.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_job = Job.objects.get(name='brake_pad_change')
        self.assertIn(new_job, maintenance_group.jobs.all())

    def test_update_maintenance_froup_assign_job(self):
        job1 = Job.objects.create(display_name='Oil Change')
        maintenance_group = MaintenanceGroup.objects.create(
            code="Custom1",
            display_name="Custom1"
        )
        maintenance_group.jobs.add(job1)

        job2 = Job.objects.create(display_name='Oil Filter Change')
        payload = {'jobs': [{'display_name': 'Oil Filter Change'}]}
        url = detail_url(maintenance_group.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(job2, maintenance_group.jobs.all())
        self.assertNotIn(job1, maintenance_group.jobs.all())

    def test_partialy_clear_jobs(self):
        """Test removing job from maintenance group"""
        job1 = Job.objects.create(display_name='Oil Change')
        job2 = Job.objects.create(display_name='Oil Filter Change')
        job3 = Job.objects.create(display_name='Air Filter Change')
        maintenance_group = MaintenanceGroup.objects.create(
            code="Custom1",
            display_name="Custom1"
        )
        maintenance_group.jobs.add(job1, job2, job3)

        payload = {
            'jobs': [
                {'display_name': 'Oil Change'},
                {'display_name': 'Oil Filter Change'},
            ]
        }
        url = detail_url(maintenance_group.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(job1, maintenance_group.jobs.all())
        self.assertIn(job2, maintenance_group.jobs.all())
        self.assertNotIn(job3, maintenance_group.jobs.all())

    def test_create_maintenance_group_without_jobs_fails(self):
        """Test that creating a maintenance group without jobs fails"""
        payload = {
            'code': 'C',
            'display_name': 'Maintenance C',
        }
        res = self.client.post(MAINTENANCE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('jobs', res.data)

    def test_create_maintenance_group_with_empty_jobs_fails(self):
        """Test that creating a maintenance group with empty jobs list fails"""
        payload = {
            'code': 'C',
            'display_name': 'Maintenance C',
            'jobs': []
        }
        res = self.client.post(MAINTENANCE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('jobs', res.data)

    def test_update_maintenance_group_without_jobs_fails(self):
        """Test that updating a maintenance group without jobs fails"""
        maintenance_group = create_maintenance_group()
        url = detail_url(maintenance_group.id)
        payload = {
            'code': 'C1',
            'display_name': 'Maintenance C1',
        }
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('jobs', res.data)

    def test_update_maintenance_group_with_empty_jobs_fails(self):
        """Test that updating a maintenance group with empty jobs list fails"""
        maintenance_group = create_maintenance_group()
        url = detail_url(maintenance_group.id)
        payload = {
            'code': 'C1',
            'display_name': 'Maintenance C1',
            'jobs': []
        }
        res = self.client.put(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('jobs', res.data)
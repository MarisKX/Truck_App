"""
Tests for jobs API
"""
# Django general imports
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
# Rest Framework imports
from rest_framework import status
from rest_framework.test import APIClient
# Custom imports
from maintenance.models import Job
from maintenance.serializers import JobSerializer


JOB_URL = reverse('maintenance:job-list')


def detail_url(job_id):
    """Create and return a job detail url"""
    return reverse('maintenance:job-detail', args=[job_id])


def create_user(email='user@example.com', password='pass1'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class PublicJobsApiTests(TestCase):
    """Test unauthenticated API requests for Jobs"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to retrieve Jobs"""
        res = self.client.get(JOB_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobsApiTests(TestCase):
    """Test authenticated API requests for Jobs"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_jobs(self):
        """Test retrieving a list of jobs"""
        Job.objects.create(display_name="Oil Change")
        Job.objects.create(display_name="Oil Filter Change")

        res = self.client.get(JOB_URL)

        jobs = Job.objects.all().order_by('name')
        serializer = JobSerializer(jobs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_job(self):
        """Test updating a tag"""
        job = Job.objects.create(display_name='Brake Pads Change')

        payload = {'display_name': 'Brake Discs Change'}
        url = detail_url(job.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        self.assertEqual(job.display_name, payload['display_name'])
        self.assertEqual(job.name, 'brake_discs_change')

    def test_delete_job(self):
        """Test deleting a job"""
        job = Job.objects.create(display_name='Air Filter Change')

        url = detail_url(job.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        jobs = Job.objects.filter(display_name='Air Filter Change')
        self.assertFalse(jobs.exists())

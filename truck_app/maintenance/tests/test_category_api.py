"""
Tests for categories API
"""
# Django general imports
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
# Rest Framework imports
from rest_framework import status
from rest_framework.test import APIClient
# Custom imports
from maintenance.models import Category
from maintenance.serializers import CategorySerializer


CATEGORY_URL = reverse('maintenance:category-list')


def detail_url(category_id):
    """Create and return a category detail url"""
    return reverse('maintenance:category-detail', args=[category_id])


def create_user(email='user@example.com', password='pass1589'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class PublicCategoriesApiTests(TestCase):
    """Test unauthenticated API requests for Categories"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to retrieve Categories"""
        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriesApiTests(TestCase):
    """Test authenticated API requests for Categories"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_category(self):
        """Test retrieving a list of category"""
        Category.objects.create(display_name="Engine")
        Category.objects.create(display_name="Brakes")

        res = self.client.get(CATEGORY_URL)

        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category(self):
        """Test creating a new category"""
        payload = {'display_name': 'Engine'}
        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        category = Category.objects.get(id=res.data['id'])
        self.assertEqual(category.display_name, payload['display_name'])
        self.assertEqual(category.name, 'engine')

    def test_update_category(self):
        """Test updating a category"""
        category = Category.objects.create(display_name='Electrics - Interior')

        payload = {'display_name': 'Electrics - Exterior'}
        url = detail_url(category.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.display_name, payload['display_name'])
        self.assertEqual(category.name, 'electrics_-_exterior')

    def test_delete_category(self):
        """Test deleting a job"""
        category = Category.objects.create(display_name='Electrics - Interior')

        url = detail_url(category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        jobs = Category.objects.filter(display_name='Electrics - Interior')
        self.assertFalse(jobs.exists())

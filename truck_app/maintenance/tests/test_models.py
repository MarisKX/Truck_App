from django.test import TestCase
from maintenance.models import Job, Category, MaintenanceGroup


class MaintenanceModelsTests(TestCase):
    """Tests for maintenance models"""

    def test_create_job(self):
        """Test that a job can be created"""
        job = Job.objects.create(
            display_name='Oil Change'
        )

        self.assertEqual(str(job), 'oil_change')
        self.assertEqual(job.get_display_name(), 'Oil Change')

    def test_create_maintenance_code_without_jobs(self):
        """
        Test creating a MaintenanceGroup without jobs
        and with a default category
        """

        code = MaintenanceGroup.objects.create(
            code='A+',
            display_name='Maintenance A+'
        )

        default_category = Category.objects.get(display_name='Uncategorized')

        self.assertEqual(code.name, 'maintenance_a+')
        self.assertEqual(code.get_display_name(), 'Maintenance A+')
        self.assertEqual(code.category, default_category)

    def test_create_category(self):
        """Test that a job can be created"""
        category = Category.objects.create(
            display_name='General Maintenance'
        )

        self.assertEqual(str(category), 'general_maintenance')
        self.assertEqual(category.get_display_name(), 'General Maintenance')

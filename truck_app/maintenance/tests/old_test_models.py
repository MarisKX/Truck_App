from django.test import TestCase
from maintenance.models import Job, MaintenanceGroup


class MaintenanceModelsTests(TestCase):
    """Tests for maintenance models"""

    def test_create_job(self):
        """Test that a job can be created"""
        job = Job.objects.create(
            name='oil_change',
            display_name='Oil Change'
        )

        self.assertEqual(str(job), 'oil_change')
        self.assertEqual(job.get_display_name(), 'Oil Change')

    def test_create_maintenance_code_without_jobs(self):
        """Test creating a MaintenanceGroup with jobs"""

        code = MaintenanceGroup.objects.create(
            code='A+',
            display_name='Maintenance A+'
        )
        name = 'maintenance_a+'

        self.assertEqual(str(name), 'maintenance_a+')
        self.assertEqual(code.get_display_name(), 'Maintenance A+')

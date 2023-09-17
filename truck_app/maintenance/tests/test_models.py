from django.test import TestCase
from maintenance.models import Job, MaintenanceCode


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

    def test_create_maintenance_code_with_jobs(self):
        """Test creating a MaintenanceCode with jobs"""

        job1 = Job.objects.create(
            display_name='Oil Change'
        )
        job2 = Job.objects.create(
            display_name='Air Filter Change'
        )

        code = MaintenanceCode.objects.create(
            code='A+',
            display_name='Maintenance A+'
        )

        code.jobs.add(job1, job2)

        self.assertEqual(code.jobs.count(), 2)
        self.assertTrue(code.jobs.filter(name='oil_change').exists())
        self.assertTrue(code.jobs.filter(name='air_filter_change').exists())

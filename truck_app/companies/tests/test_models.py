from django.test import TestCase
from companies.models import Company, CompanyLocation


class CompanyModelTests(TestCase):
    """Test Company model"""

    def test_save_method(self):
        """Test save method replaces spaces with underscores in name"""
        company = Company.objects.create(
            display_name="Test Company",
            registration_number="12345",
            vat_number="GB123456789",
            adress_1="123 Test Street",
            city_town="Test Town",
            province_state="Test State",
            post_code="TE1 1ST",
            country='GB'
        )

        self.assertEqual(company.name, "test_company")

    def test_get_display_name(self):
        """Test get_display_name method returns the display_name attribute"""
        company = Company.objects.create(
            display_name="Test Company",
            registration_number="12345",
            vat_number="GB123456789",
            adress_1="123 Test Street",
            city_town="Test Town",
            province_state="Test State",
            post_code="TE1 1ST",
            country='GB'
        )

        self.assertEqual(company.get_display_name(), "Test Company")


class CompanyLocationModelTests(TestCase):
    """Test CompanyLocation model"""

    def test_save_method(self):
        """Test save method replaces spaces with underscores in name"""
        company = Company.objects.create(
            display_name="Test Company",
            registration_number="12345",
            vat_number="GB123456789",
            adress_1="123 Test Street",
            city_town="Test Town",
            province_state="Test State",
            post_code="TE1 1ST",
            country='GB'
        )

        location = CompanyLocation.objects.create(
            company=company,
            display_name="Test Location",
            location_code="LOC1",
            adress_1="456 Test Avenue",
            city_town="Test City",
            province_state="Test State",
            post_code="TE2 2ST",
            country='GB'
        )

        self.assertEqual(location.name, "test_location")

    def test_get_display_name(self):
        """Test get_display_name method returns the display_name attribute"""
        company = Company.objects.create(
            display_name="Test Company",
            registration_number="12345",
            vat_number="GB123456789",
            adress_1="123 Test Street",
            city_town="Test Town",
            province_state="Test State",
            post_code="TE1 1ST",
            country='GB'
        )

        location = CompanyLocation.objects.create(
            company=company,
            display_name="Test Location",
            location_code="LOC1",
            adress_1="456 Test Avenue",
            city_town="Test City",
            province_state="Test State",
            post_code="TE2 2ST",
            country='GB'
        )

        self.assertEqual(location.get_display_name(), "Test Location")

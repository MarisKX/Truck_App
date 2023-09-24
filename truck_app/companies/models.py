"""
Database Companies models
"""
from django.db import models
from django_countries.fields import CountryField


class Company(models.Model):
    """Company data"""
    class Meta:
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=30, unique=True)
    vat_number = models.CharField(max_length=30, verbose_name='VAT')
    adress_1 = models.CharField(max_length=255, verbose_name='Street Adress')
    city_town = models.CharField(max_length=255, verbose_name='City/Town')
    province_state = models.CharField(
        max_length=255,
        verbose_name='State/Province/Region')
    post_code = models.CharField(max_length=255, verbose_name='Postal Code')
    country = CountryField(blank_label='(Select Country)')

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class CompanyLocation(models.Model):
    """Company Locations data"""
    class Meta:
        verbose_name_plural = 'Company Loacations'

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    location_code = models.CharField(max_length=30)
    adress_1 = models.CharField(max_length=255, verbose_name='Street Adress')
    city_town = models.CharField(max_length=255, verbose_name='City/Town')
    province_state = models.CharField(
        max_length=255,
        verbose_name='State/Province/Region')
    post_code = models.CharField(max_length=255, verbose_name='Postal Code')
    country = CountryField(blank_label='(Select Country)')

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)

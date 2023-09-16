"""
Database truck models.
"""
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Truck(models.Model):
    """Truck Objects"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Last Edit By',
        on_delete=models.PROTECT,
        default=1)
    licence_plate = models.CharField(max_length=12)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ])
    vin = models.CharField(max_length=17, unique=True)

    color = models.CharField(max_length=30, blank=True, null=True)
    engine = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.licence_plate

"""
Database truck models.
"""
from django.conf import settings
from django.db import models


class Truck(models.Model):
    """Truck Objects"""
    last_edit = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=1)
    licence_plate = models.CharField(max_length=12)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    vin = models.CharField(max_length=17)

    def __str__(self):
        return self.licence_plate

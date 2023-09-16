"""
Django admin customization
"""
# Django imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _  # noqa
# Custom imports
from trucks.models import Truck


class TruckAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )
    list_display = (
        'licence_plate',
        'make',
        'model',
        'year',
        'vin',
    )


admin.site.register(Truck, TruckAdmin)

"""
Django admin customization
"""
# Django imports
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Custom imports
from trucks.models import Truck


class TruckAdmin(admin.ModelAdmin):
    readonly_fields = ('last_edit', )
    list_display = (
        'licence_plate',
        'make',
        'model',
        'year',
        'vin',
    )


admin.site.register(Truck, TruckAdmin)
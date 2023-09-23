"""
Django admin customization
"""
# Django imports
from django.contrib import admin
# Custom imports
from trucks.models import Truck, MaintenanceLog


class MaintenanceLogAdmin(admin.TabularInline):
    model = MaintenanceLog
    readonly_fields = (
        'id',
        'log_number',
    )


class TruckAdmin(admin.ModelAdmin):
    inlines = (MaintenanceLogAdmin, )
    readonly_fields = ('user', )
    list_display = (
        'licence_plate',
        'make',
        'model',
        'year',
        'vin',
        'color',
        'engine',
        'fuel',
        'transmission',
        'body_style',
    )
    ordering = ('licence_plate', )


admin.site.register(Truck, TruckAdmin)

"""
Django admin customization
"""
# Django imports
from django.contrib import admin
# Custom imports
from maintenance.models import Job, MaintenanceCode


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    readonly_fields = ('name',)
    ordering = ('name',)


@admin.register(MaintenanceCode)
class MaintenanceCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('name',)
    list_display = ('code', 'display_name', 'name')

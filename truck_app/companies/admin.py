"""
Django admin customization
"""
# Django imports
from django.contrib import admin
# Custom imports
from .models import Company, CompanyLocation


class CompanyLocationAdmin(admin.TabularInline):
    model = CompanyLocation
    readonly_fields = (
        'name',
    )


class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyLocationAdmin, )
    ordering = ['name', ]
    list_display = ['display_name', ]
    readonly_fields = ['name', 'id', ]
    ordering = ('id', )


admin.site.register(Company, CompanyAdmin)

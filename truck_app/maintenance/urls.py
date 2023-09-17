"""
URL mappings for the jobs/maintenance app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from maintenance import views


router = DefaultRouter()
router.register('maintenance_code', views.MaintenanceGroupViewSet)
# router.register('jobs', views.JobViewSet)

app_name = 'maintenance'

urlpatterns = [
    path('', include(router.urls))
]

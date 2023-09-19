"""
URL mappings for the jobs/maintenance app
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from maintenance import views


router = DefaultRouter()
router.register('maintenance_groups', views.MaintenanceGroupViewSet)
router.register('jobs', views.JobViewSet)
router.register('categories', views.CategoryViewSet)

app_name = 'maintenance'

urlpatterns = [
    path('', include(router.urls))
]

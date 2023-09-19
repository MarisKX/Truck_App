from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MaintenanceGroup, Category


@receiver(post_save, sender=MaintenanceGroup)
def set_default_category(sender, instance, **kwargs):
    if instance.category is None:
        uncategorized, created = Category.objects.get_or_create(
            display_name='Uncategorized')
        instance.category = uncategorized
        instance.save()

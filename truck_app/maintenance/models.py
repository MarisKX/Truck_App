"""
Database maintence and jobs models.
"""
from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class Job(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the name
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)


class MaintenanceGroup(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    jobs = models.ManyToManyField(Job, related_name='maintenance_groups')

    def __str__(self):
        return self.code

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the values
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)

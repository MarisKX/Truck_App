"""
Database maintence and jobs models.
"""
from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    display_name = models.CharField(max_length=100, unique=True)

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
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    # jobs = models.ManyToManyField(Job, related_name='jobs')

    def __str__(self):
        return self.code

    def get_display_name(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the article
        """
        self.name = self.display_name.replace(" ", "_").lower()
        super().save(*args, **kwargs)

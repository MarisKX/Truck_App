# Generated by Django 3.2.21 on 2023-09-19 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0006_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancegroup',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.category'),
        ),
    ]
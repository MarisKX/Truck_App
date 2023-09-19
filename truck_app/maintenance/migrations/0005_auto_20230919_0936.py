# Generated by Django 3.2.21 on 2023-09-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0004_maintenancegroup_jobs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('display_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='job',
            name='display_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='maintenancegroup',
            name='jobs',
            field=models.ManyToManyField(related_name='maintenance_groups', to='maintenance.Job'),
        ),
    ]
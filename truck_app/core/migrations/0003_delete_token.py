# Generated by Django 3.2.21 on 2023-09-21 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]

# Generated by Django 3.2.21 on 2023-09-16 21:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0004_auto_20230916_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)]),
        ),
    ]

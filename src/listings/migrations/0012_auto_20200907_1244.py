# Generated by Django 3.1 on 2020-09-07 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_listing_contact_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='contact_details',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(11, 'contact details length must be greater than 11 characters')]),
        ),
    ]
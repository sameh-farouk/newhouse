# Generated by Django 3.1 on 2020-09-07 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_auto_20200907_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='contact_details',
            field=models.TextField(default='010165211xx whatsapp only', validators=[django.core.validators.MinLengthValidator(11, 'contact details length must be greater than 11 characters')]),
            preserve_default=False,
        ),
    ]

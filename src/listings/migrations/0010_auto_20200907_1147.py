# Generated by Django 3.1 on 2020-09-07 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_auto_20200907_0307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='propty',
            old_name='address',
            new_name='street_address',
        ),
    ]

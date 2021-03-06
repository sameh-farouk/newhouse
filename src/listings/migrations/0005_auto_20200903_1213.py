# Generated by Django 3.1 on 2020-09-03 10:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_auto_20200903_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='url',
            field=models.ImageField(default='', upload_to='uploads/%Y/%m/%d', validators=[django.core.validators.validate_image_file_extension]),
            preserve_default=False,
        ),
    ]

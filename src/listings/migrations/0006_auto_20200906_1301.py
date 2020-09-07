# Generated by Django 3.1 on 2020-09-06 11:01

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20200903_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='destrict',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='governorate', chained_model_field='governorate', on_delete=django.db.models.deletion.CASCADE, show_all=True, to='listings.destrict'),
        ),
    ]

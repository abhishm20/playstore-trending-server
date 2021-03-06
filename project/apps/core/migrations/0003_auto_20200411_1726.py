# Generated by Django 3.0.4 on 2020-04-11 17:26

import core.utility.date_util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200411_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='created_at',
            field=models.DateTimeField(blank=True, default=core.utility.date_util.get_current_time, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='package_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='refreshed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='packageattachment',
            name='created_at',
            field=models.DateTimeField(blank=True, default=core.utility.date_util.get_current_time, null=True),
        ),
    ]

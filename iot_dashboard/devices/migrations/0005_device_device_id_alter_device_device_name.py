# Generated by Django 4.2.3 on 2023-07-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_remove_device_last_data_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]

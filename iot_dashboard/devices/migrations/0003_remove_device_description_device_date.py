# Generated by Django 4.2.3 on 2023-07-23 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_rename_last_updated_device_last_data_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='description',
        ),
        migrations.AddField(
            model_name='device',
            name='date',
            field=models.DateField(null=True),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-26 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0010_alter_realtimedata_device'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='date',
        ),
    ]

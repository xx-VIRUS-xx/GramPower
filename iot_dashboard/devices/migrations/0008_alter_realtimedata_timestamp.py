# Generated by Django 4.2.3 on 2023-07-24 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_realtimedata_delete_datapoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtimedata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

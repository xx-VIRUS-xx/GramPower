# Generated by Django 4.2.3 on 2023-07-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0012_alter_device_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='status',
            field=models.CharField(choices=[('live', 'Live'), ('down', 'Down')], max_length=20),
        ),
    ]
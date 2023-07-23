# models.py
from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=100,null=True)
    date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=[('live', 'Live'), ('down', 'Down')],null=True)
    last_data_timestamp = models.DateTimeField()

    # Add more fields as needed, such as device type, location, etc.

    def __str__(self):
        return self.device_name

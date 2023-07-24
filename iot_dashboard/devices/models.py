# models.py
from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=100,unique=True,null=True)
    date = models.DateField(null=True)
    device_id = models.CharField(max_length=20, unique=True,null=True)
    status = models.CharField(max_length=20, choices=[('live', 'Live'), ('down', 'Down')],null=True)
   

    # Add more fields as needed, such as device type, location, etc.

    def __str__(self):
        return self.device_name

class RealTimeData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE,to_field='device_id')
    current = models.FloatField(null=True)
    voltage = models.FloatField(null=True)
    power = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.device_name
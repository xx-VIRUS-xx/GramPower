# models.py
from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=100,unique=True,null=True)
    device_id = models.CharField(max_length=20, unique=True, null=True)
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.device_name

class RealTimeData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE,to_field='device_id')
    current = models.FloatField(null=True)
    voltage = models.FloatField(null=True)
    power = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.device.device_name} - {self.timestamp}"
import random
from django.core.management.base import BaseCommand
from devices.models import Device,RealTimeData

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Clear existing device data
        RealTimeData.objects.all().delete()

        device_ids = Device.objects.values_list('device_id', flat=True)

        while True: 
            device1 = random.choice(device_ids)
            device = Device.objects.get(device_id=device1)
            current = random.uniform(0.0, 10.0)
            voltage = random.uniform(110.0, 240.0)
            power = current * voltage
            RealTimeData.objects.create(device=device, current=current, voltage=voltage, power=power)
        


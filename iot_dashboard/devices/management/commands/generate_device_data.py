
from django.core.management.base import BaseCommand
from devices.models import Device

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Clear existing devices and device data
        Device.objects.all().delete()

        # Generate and save 100 random devices
        devices = []
        device_ids=[]
        for i in range(100):
            name = f"Device-{i+1}"
            device_id = f"gram-{i+1}"
            device_ids.append(device_id)
            device_data = Device.objects.create(device_name=name, device_id=device_id)
            devices.append(device_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated random data for 100 devices.'))

       
from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name', 'date', 'status', 'last_data_timestamp']  # Include all fields here

        # Optional: You can add widgets or customize the form fields as needed
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'last_data_timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

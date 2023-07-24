from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Sum
from .models import Device,RealTimeData
from .forms import DeviceForm
from datetime import datetime, timedelta
from django.http import JsonResponse

import random

# Function to generate random data
def generate_data():
    current = random.uniform(0, 10)
    voltage = random.uniform(100, 250)
    power = current * voltage
    timestamp = datetime.now()
    return current, voltage, power, timestamp

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    devices = Device.objects.all()
    return render(request, 'dashboard.html', {'devices': devices})

@login_required
def device_detail(request, device_id=None):
    # Retrieve the device if device_id is provided
    if device_id:
        device = get_object_or_404(Device, pk=device_id)
    else:
        device = None

    # Check if the user is a superuser and if the request method is POST
    if request.user.is_superuser and request.method == 'POST':
        # If the form is submitted with data, process the form and add the device
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Device added successfully!')
            return redirect('device_detail', device_id=form.instance.id)
    else:
        # Otherwise, show the device details (if device_id is provided) or the add device form
        if device_id:
            form = DeviceForm(instance=device)  # Prepopulate the form with device details
        else:
            form = DeviceForm()

    return render(request, 'device_detail.html', {'form': form, 'device': device})

@login_required
def real_time_data(request):
    device_ids = Device.objects.values_list('device_id', flat=True)
    device_id = random.choice(device_ids)

    current, voltage, power, timestamp = generate_data()

    RealTimeData.objects.create(device_id=device_id, current=current, voltage=voltage, power=power)

    # Get the average current and voltage
    avg_current = RealTimeData.objects.filter(device_id=device_id).aggregate(Avg('current'))['current__avg']
    avg_voltage = RealTimeData.objects.filter(device_id=device_id).aggregate(Avg('voltage'))['voltage__avg']

    # Get the total power
    total_power = RealTimeData.objects.filter(device_id=device_id).aggregate(Sum('power'))['power__sum']

    # Create the data dictionary
    data = {
        'timestamp': str(timestamp),
        'avg_current': float(avg_current) if avg_current is not None else None,
        'avg_voltage': float(avg_voltage) if avg_voltage is not None else None,
        'total_power': float(total_power) if total_power is not None else None,
    }

    return JsonResponse(data)

@login_required
def show_real_time_data(request,device_id):
    devices = get_object_or_404(Device, pk=device_id)
    data_dict = {}

    try:
        timestamp = RealTimeData.objects.filter(device=devices).latest('timestamp')
        total_power = RealTimeData.objects.filter(device=devices).aggregate(Sum('power'))['power__sum']
        avg_current = RealTimeData.objects.filter(device=devices).aggregate(Avg('current'))['current__avg']
        avg_voltage = RealTimeData.objects.filter(device=devices).aggregate(Avg('voltage'))['voltage__avg']

        data_dict[devices] = {
            'timestamp': timestamp,
            'avg_current': avg_current,
            'avg_voltage': avg_voltage,
            'total_power': total_power
        }

    except RealTimeData.DoesNotExist:
        # Handle the case when no RealTimeData is available for the device
        data_dict[devices] = {
            'timestamp': None,
            'avg_current': None,
            'avg_voltage': None,
            'total_power': None
        }

    return render(request, 'real_time.html', {'data_dict': data_dict,'devices':devices})


    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()  # Save the newly registered user
            login(request, new_user)  # Log in the user
            return redirect('login_page')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

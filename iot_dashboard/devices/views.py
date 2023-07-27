from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Avg, Sum
from .models import Device,RealTimeData
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.http import JsonResponse

import pytz
import random
        

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

    device_ids = Device.objects.values_list('device_id', flat=True)

    for _ in range(70): 
        device1 = random.choice(device_ids)
        device = Device.objects.get(device_id=device1)
        current = random.uniform(0.0, 10.0)
        voltage = random.uniform(110.0, 240.0)
        power = current * voltage
        RealTimeData.objects.create(device=device, current=current, voltage=voltage, power=power)
        
    for device in devices:
        latest_data = RealTimeData.objects.filter(device=device).order_by('-timestamp').first()
        if latest_data:
            time_diff = now() - latest_data.timestamp
            if time_diff.total_seconds() <= 100:
                device.status = "Live"
            else:
                device.status = "Down"
        else:
            device.status = "Down"
        device.save()

    context = {'devices': devices}
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = [{ 'status': device.status,'name':device.device_name,'id':device.device_id} for device in devices]
        return JsonResponse(data, safe=False)
    return render(request, 'dashboard.html', context)

@login_required
def real_time_data(request):
    device_id = request.GET.get('device_id')

    # If device_id is not provided, select a random device
    if not device_id:
        device_ids = Device.objects.values_list('device_id', flat=True)
        device_id = random.choice(device_ids)

    current = random.uniform(0, 10)
    voltage = random.uniform(100, 250)
    power = current * voltage
    timestamp = datetime.now()

    RealTimeData.objects.create(device_id=device_id, current=current, voltage=voltage, power=power)

    # Get the average current and voltage
    avg_current = RealTimeData.objects.filter(device_id=device_id).aggregate(Avg('current'))['current__avg']
    avg_voltage = RealTimeData.objects.filter(device_id=device_id).aggregate(Avg('voltage'))['voltage__avg']

    # Get the total power
    total_power = RealTimeData.objects.filter(device_id=device_id).aggregate(Sum('power'))['power__sum']

    ist = pytz.timezone('Asia/Kolkata')

    time_threshold = now() - timedelta(minutes=1)
    data = RealTimeData.objects.filter(device_id=device_id, timestamp__gte=time_threshold).order_by('timestamp')

    # Prepare data for the graph
    time_labels = [entry.timestamp.astimezone(ist).strftime('%H:%M:%S') for entry in data]
    power_data = [entry.power for entry in data]

    # Create the data dictionary
    data = {
        'time_labels':time_labels,
        'power_data':power_data,
        'timestamp': str(timestamp),
        'avg_current': float(avg_current) if avg_current is not None else None,
        'avg_voltage': float(avg_voltage) if avg_voltage is not None else None,
        'total_power': float(total_power) if total_power is not None else None,
    }

    return JsonResponse(data)

@login_required
def show_real_time_data(request, device_id):
    devices = get_object_or_404(Device, device_id=device_id)
    data_dict = {}

    if devices.status == 'Live':
        latest_data = RealTimeData.objects.filter(device=devices).latest('timestamp')
        total_power = RealTimeData.objects.filter(device=devices).aggregate(Sum('power'))['power__sum']
        avg_current = RealTimeData.objects.filter(device=devices).aggregate(Avg('current'))['current__avg']
        avg_voltage = RealTimeData.objects.filter(device=devices).aggregate(Avg('voltage'))['voltage__avg']
        data_dict[devices] = {
            'timestamp': latest_data.timestamp,
            'avg_current': avg_current,
            'avg_voltage': avg_voltage,
            'total_power': total_power,
            'status': 'Live',  # Add the 'status' key with value 'Live'
        }

    else:
        # Device is down, clear previous real-time data
        RealTimeData.objects.filter(device=devices).delete()

        # Set real-time data as None
        data_dict[devices] = {
            'timestamp': None,
            'avg_current': None,
            'avg_voltage': None,
            'total_power': None,
            'status': 'Down',  # Add the 'status' key with value 'Down'
        }

    return render(request, 'real_time.html', {'data_dict': data_dict, 'devices': devices})


@login_required 
def graph(request):
    device_id = request.GET.get('device_id')
    data_dict={}

    time_threshold = now() - timedelta(minutes=1)
    data = RealTimeData.objects.filter(device=device_id, timestamp__gte=time_threshold).order_by('timestamp')

    # Prepare data for the graph
    time_labels = [entry.timestamp.strftime('%H:%M:%S') for entry in data]
    power_data = [entry.power for entry in data]

    data_dict[device_id]={
        "time": time_labels,
        "power" : power_data
    }

    return render(request, 'graph.html', { 'data_dict':data_dict, 'devices': device_id,})
   

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

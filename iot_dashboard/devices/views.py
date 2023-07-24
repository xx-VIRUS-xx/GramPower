from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Sum
from .models import Device,RealTimeData
from .forms import DeviceForm

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
def real_time_graph(request, device_id=None):
    device = get_object_or_404(Device, pk=device_id)
    real_time_data = RealTimeData.objects.filter(device=device)

    avg_current = real_time_data.aggregate(avg_current=Avg('current'))['avg_current']
    avg_voltage = real_time_data.aggregate(avg_voltage=Avg('voltage'))['avg_voltage']
    total_power = real_time_data.aggregate(total_power=Sum('power'))['total_power']
    return render(request, 'real_time.html', {
        'device': device,
        'real_time_data': real_time_data,
        'avg_current': avg_current,
        'avg_voltage': avg_voltage,
        'total_power': total_power,
    })

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

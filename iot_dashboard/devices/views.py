from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Device
from .forms import DeviceForm

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()  # Save the newly registered user
                login(request, new_user)  # Log in the user
                return redirect('login_page')  # Redirect to login page
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
    if request.method == 'POST' and request.user.is_superuser:
        # Add device handling logic here
        # Example: device_name = request.POST['device_name']
        # Add the device to the database
        messages.success(request, "Device added successfully!")
        return redirect('dashboard')

    if device_id:
        device = Device.objects.get(pk=device_id)

    # Check if the user is a superuser before displaying the form
    if request.user.is_superuser and request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_detail', device_id=device_id)
    else:
        form = DeviceForm()

    return render(request, 'device_detail.html', {'form': form})

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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page for combined registration and login
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('devices/add/', views.device_detail, name='add_device'),  # URL for adding a new device
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('show_real_time_data/<int:device_id>/', views.show_real_time_data, name='show_real_time_data'),
    path('real_time_data/', views.real_time_data, name='real_time_data'),
]

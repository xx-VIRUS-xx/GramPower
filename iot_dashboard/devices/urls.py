# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('show_real_time_data/<str:device_id>/', views.show_real_time_data, name='show_real_time_data'),
    path('real_time_data/', views.real_time_data, name='real_time_data'),
    path('graph/<str:device_id>/', views.graph, name='graph'),
]

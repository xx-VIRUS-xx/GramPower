# routing.py
# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/real_time_data/<int:device_id>/', consumers.RealTimeDataConsumer.as_asgi()),
]

# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from devices.consumers import RealTimeDataConsumer
from django.urls import path

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        # Add WebSocket route for real-time data consumer
        path('ws/real_time_data/', RealTimeDataConsumer.as_asgi()),
    ]),
})

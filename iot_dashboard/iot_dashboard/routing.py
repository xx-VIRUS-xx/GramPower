from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from devices.consumers import DeviceConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                # Add WebSocket URL patterns here
                # Example: path('ws/devices/<int:device_id>/', DeviceConsumer.as_asgi()),
            ]
        )
    ),
})

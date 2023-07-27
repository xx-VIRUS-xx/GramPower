# iot_dashboard/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from devices import routing  # Import your app's routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routing.websocket_urlpatterns),  # Use the URL patterns from your app's routing
})

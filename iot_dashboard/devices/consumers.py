# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RealTimeData

class RealTimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.group_name = f'device_{self.device_id}'

        # Add the user to the WebSocket group to receive updates
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the WebSocket group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass  # This consumer does not receive data from the client

    async def send_real_time_data(self, event):
        # Send real-time data to the client
        latest_data = RealTimeData.objects.latest('timestamp')
        real_time_data = {
            'current': latest_data.current,
            'voltage': latest_data.voltage,
            'power': latest_data.power,
            'timestamp': latest_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Send real-time data to the WebSocket
        await self.send(text_data=json.dumps(real_time_data))

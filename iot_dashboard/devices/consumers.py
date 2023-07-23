from channels.generic.websocket import AsyncWebsocketConsumer

class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def send_live_data(self, event):
        pass

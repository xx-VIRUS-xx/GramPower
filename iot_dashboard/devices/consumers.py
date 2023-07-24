# consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class RealTimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Perform any necessary authentication here (if needed)
        await self.accept()

        await self.send_sample_data()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Process the received data and save it to the database
        # You can call the handle_real_time_data function from views.py here
    async def send_sample_data(self):
        while True:
            # Replace this part with your actual data retrieval logic
            # For demonstration purposes, we're sending sample data
            sample_data = {
                'current': 10.0,  # Sample current value
                'voltage': 220.0,  # Sample voltage value
                'power': 2200.0,  # Sample power value
                'timestamp': '2023-07-31 12:34:56'  # Sample timestamp
            }

            # Send the sample data as a JSON string to the client
            await self.send(text_data=json.dumps(sample_data))

            # Wait for 5 seconds before sending the next sample data
            await asyncio.sleep(5)
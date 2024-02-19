import asyncio
from websockets import connect
from websockets.client import WebSocketClientProtocol

class SocketClient:
    def __init__(self, server_address: str):
        self.server_address = server_address
        self.websocket: WebSocketClientProtocol = None
        self.callbacks = []

    async def connect(self):
        async with connect(self.server_address) as websocket:
            self.websocket = websocket
            print('CLIENT: Connected to the server.')
            
            # Send a message to the server
            await self.send_message('Hello, server!')
            
            # Start checking for messages
            await self.check_for_messages()

    async def send_message(self, message: str):
        try:
            await self.websocket.send(message)
            print(f'CLIENT: Sent message: {message}')
        except Exception as e:  # Catch more specific exceptions as needed
            print(f'CLIENT: Failed to send message. Error: {e}')

    async def receive_message(self):
        try:
            response = await self.websocket.recv()
            print(f'CLIENT: Received response: {response}')

            # Call all registered callbacks with the received message
            for callback in self.callbacks:
                callback(response)

            return response

        except Exception as e:  # Catch more specific exceptions as needed
            print(f'CLIENT: Failed to receive message. Error: {e}')

    async def check_for_messages(self):
        try:
            while True:
                await self.receive_message()
                await asyncio.sleep(1)  # Adjust as necessary
        except Exception as e:
            print(f'CLIENT: Error checking messages. Error: {e}')
            await self.close()

    async def close(self):
        await self.websocket.close()
        print('CLIENT: Connection closed.')

    def register_callback(self, callback):
        self.callbacks.append(callback)
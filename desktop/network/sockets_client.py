import asyncio
import logging
from typing import List, Callable
from websockets import connect
from websockets.client import WebSocketClientProtocol

logger = logging.getLogger(__name__)

class SocketClient:
    def __init__(self, server_address: str):
        self.server_address: str = server_address
        self.websocket: WebSocketClientProtocol | None = None
        self.callbacks: List[Callable[[str], None]] = []

    async def connect(self):
        try:
            async with connect(self.server_address) as websocket:
                self.websocket = websocket
                logger.info('CLIENT: Connected to the server.')

                await self.send_message('Hello, server!')
                await self.check_for_messages()
        except Exception as e:
            logger.error(f'CLIENT: Failed to connect or error during message handling. Error: {e}')

    async def send_message(self, message: str):
        if self.websocket:
            try:
                await self.websocket.send(message)
                logger.info(f'CLIENT: Sent message: {message}')
            except Exception as e:
                logger.error(f'CLIENT: Failed to send message. Error: {e}')

    async def receive_message(self):
        if self.websocket:
            try:
                response = await self.websocket.recv()
                logger.info(f'CLIENT: Received response: {response}')

                # Execute callbacks concurrently
                await asyncio.gather(*(callback(response) for callback in self.callbacks))

                return response
            except Exception as e:
                logger.error(f'CLIENT: Failed to receive message. Error: {e}')

    async def check_for_messages(self):
        while self.websocket:
            await self.receive_message()

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logger.info('CLIENT: Connection closed.')

    def register_callback(self, callback: Callable[[str], None]):
        self.callbacks.append(callback)

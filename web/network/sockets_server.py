import asyncio
import logging
from typing import Set, Dict, Any

import websockets
from websockets.legacy.server import WebSocketServerProtocol

from network.shared_resources import pending_notifications

from nicegui import ui

CONNECTIONS: Set[WebSocketServerProtocol] = set()

# Initialize simpler logging as per the new preference
logging.basicConfig(level=logging.INFO, format='SERVER: %(message)s')
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

class SocketsServer:
    def __init__(self):
        logger.info("SocketsServer initialized")

    async def handle_message(self, websocket: WebSocketServerProtocol) -> None:
        while True:
            try:
                message = await websocket.recv()
                logger.info(f"Received message: {message}")

                first_word = message.split(" ")[0]
                if first_word == "Success":
                    pending_notifications[len(pending_notifications) + 1] = {"message": message, "type": "positive"}

                response = f"SERVER received: {message}"
                await websocket.send(response)

            except websockets.exceptions.ConnectionClosed as e:
                logger.info(f"Connection closed with error: {e}")
                CONNECTIONS.remove(websocket)
                break
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                break

    async def send_message(self, message: str) -> None:
        disconnected_sockets = set()
        for websocket in CONNECTIONS:
            try:
                await websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_sockets.add(websocket)
        CONNECTIONS.difference_update(disconnected_sockets)
        
        logger.info(f"Sent message to {len(CONNECTIONS)} clients")

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        CONNECTIONS.add(websocket)
        logger.info(f"New connection from {websocket.remote_address}")

        await self.handle_message(websocket)

    async def start_server(self) -> None:
        server = await websockets.serve(self.handle_connection, "localhost", 8765)
        logger.info("WebSocket server started")
        await server.wait_closed()

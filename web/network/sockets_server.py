import asyncio
from typing import Set

import websockets
from websockets.server import WebSocketServerProtocol

CONNECTIONS: Set[WebSocketServerProtocol] = set()

class SocketsServer():
    async def handle_message(self, websocket: WebSocketServerProtocol) -> None:
        while True:
            try:
                message = await websocket.recv()
                # Process the received message here
                print(f"SERVER: Received message: {message}")
                
                # Send a response back to the client
                response = f"SERVER received: {message}"
                await websocket.send(response)
                
            except websockets.exceptions.ConnectionClosed:
                # Remove the closed connection from the set
                CONNECTIONS.remove(websocket)
                break

    async def send_message(self, message: str) -> None:
        for websocket in CONNECTIONS:
            await websocket.send(message)
        
        print(f"SERVER: Sent message to {len(CONNECTIONS)} clients")

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        # Add the new connection to the set
        CONNECTIONS.add(websocket)
        
        # Print a message to the console
        print(f"SERVER: New connection from {websocket.remote_address}")

        # Start handling messages for this connection
        await self.handle_message(websocket)

    async def start_server(self) -> None:
        # Start the WebSocket server
        async with websockets.serve(self.handle_connection, "localhost", 8765):
            print("SERVER: WebSocket server started")
            await asyncio.Future()  # Keep the server running indefinitely

# Create an instance of the Sockets class and start the server
#sockets = Sockets()
#asyncio.run(sockets.start_server())

import os
import sys

from network.sockets_client import SocketClient
from system.cleaner import Cleaner

class MeridiumApp():
    def __init__(self):
        self.name = "Meridium"
        self.sockets = SocketClient(server_address=f"ws://localhost:8765")
        self.cleaner = Cleaner()
        self.sockets.register_callback(self.read_message)

    async def run(self):
        print(f"{self.name} is running")
        # start socket server to communicate with web app
        await self.sockets.connect()

    async def read_message(self, message: str):
        firstWord = message.split(" ")[0]
        if firstWord == "cleanTempFiles":
            print("Received message from web app to clean temp files")

            # send message to web app for it to process what it needs to.
            await self.cleaner.clean_temp_files(message)
    
        
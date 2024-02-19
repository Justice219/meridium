import os
import sys

from network.sockets_client import SocketClient
from system.cleaner import Cleaner

class MeridiumApp:
    def __init__(self):
        self.name = "Meridium Desktop App"
        self.socket_client = SocketClient(server_address="ws://localhost:8765")
        self.cleaner = Cleaner(self.socket_client)
        self.socket_client.register_callback(self.handle_message)

    async def run(self):
        print(f"{self.name} is running")
        await self.socket_client.connect()

    async def handle_message(self, message: str):
        command, *args = message.split(" ")
        action_map = {
            "cleanTempFiles": lambda: self.cleaner.clean_temp_files(message),
            "cleanCacheFiles": self.cleaner.clean_cache_files,  # Assumes no args needed
            "emptyRecycleBin": self.cleaner.empty_recycle_bin,  # Assumes no args needed
            "cleanBrowserData": lambda: self.cleaner.clean_browser_data(message),
        }

        if command in action_map:
            action = action_map[command]
            # Log the action dynamically
            action_description = command[4:].lower().replace('files', '').replace('data', '').replace('_', ' ')
            print(f"CLIENT: Received message from web app to {action_description}")

            # Call the action with or without "message" based on its requirement
            if callable(action):
                await action()  # Calls the lambda or function directly
            else:
                print(f"CLIENT: Unknown command or mismatch in parameters for: {command}")
        else:
            print(f"CLIENT: Unknown command: {command}")


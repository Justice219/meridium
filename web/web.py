from pages import *
import router as router_c
import asyncio
from network.sockets_server import SocketsServer 
from network.shared_resources import pending_notifications

from nicegui import app, ui

class WebApp:
    def __init__(self):
        self.app = app
        self.ui = ui
        self.home = self.create_page('/', home.content)
        self.clean = self.create_page('/clean', clean.content)
        self.tweaks = self.create_page('/tweaks', tweaks.content)
        self.pages = [self.home, self.clean, self.tweaks]
        self.sockets = SocketsServer()
        
        #asyncio.run(self.sockets.start_server())

    def create_page(self, path: str, content: callable) -> None:
        @self.ui.page(path)
        def page() -> None:
            content(self.ui, self.app, self.sockets)

    def notify(self, message: str, type: str) -> None:
        self.ui.notify(message, type=type)

    async def check_notifications(self) -> None:
        while True:
            print("SERVER: Checking for notifications...")
            # Copy keys to avoid RuntimeError due to change in dictionary size during iteration
            keys = list(pending_notifications.keys())
            for key in keys:
                if key in pending_notifications:  # Check if key still exists
                    notification = pending_notifications.pop(key)  # Safely remove the notification
                    self.notify("test", "positive")
            await asyncio.sleep(1)  # Wait for 1 second before checking again


    def run(self):
        self.app.include_router(router_c.router)
        self.app.on_startup(self.sockets.start_server)
        self.app.on_startup(self.check_notifications)
        self.ui.run(title='Meridium Web App')

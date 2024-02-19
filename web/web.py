from pages import *
import router as router_c
from network.sockets_server import SocketsServer 

from nicegui import app, ui

class WebApp:
    def __init__(self):
        self.app = app
        self.ui = ui
        self.home = self.create_page('/', home.content)
        self.clean = self.create_page('/clean', clean.content)
        self.tweaks = self.create_page('/tweaks', tweaks.content)
        self.sockets = SocketsServer()

    def create_page(self, path: str, content: callable) -> None:
        @self.ui.page(path)
        def page() -> None:
            content(self.ui, self.app, self.sockets)

    def run(self):
        self.app.include_router(router_c.router)
        self.app.on_startup(self.sockets.start_server)
        self.ui.run(title='Meridium Web App')

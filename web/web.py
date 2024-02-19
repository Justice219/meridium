from pages import home, clean, tweaks  # Explicitly import the needed modules
import router as router_c
import asyncio
from network.sockets_server import SocketsServer
from network.shared_resources import pending_notifications

from nicegui import app, ui

class WebApp:
    """A web application built with NiceGUI for managing different pages and socket communications."""

    def __init__(self):
        self.app = app
        self.ui = ui
        self.router = router_c.router  # Use a more descriptive name for the router
        self.sockets = SocketsServer()
        self.initialize_pages()

    def initialize_pages(self) -> None:
        """Initializes the pages of the web application."""
        self.pages = {
            '/': home.content,
            '/clean': clean.content,
            '/tweaks': tweaks.content,
        }
        for path, content in self.pages.items():
            self.create_page(path, content)

    def create_page(self, path: str, content_callable: callable) -> None:
        """Creates a page for the web application.

        Args:
            path: The URL path for the page.
            content_callable: A callable that defines the content of the page.
        """
        @self.ui.page(path)
        def page() -> None:
            content_callable(self.ui, self.app, self.sockets)

    def notify(self, message: str, notification_type: str) -> None:
        """Sends a notification through the UI.

        Args:
            message: The notification message.
            notification_type: The type of notification (e.g., 'info', 'error').
        """
        self.ui.notify(message, type=notification_type)

    def run(self) -> None:
        """Runs the web application."""
        self.app.include_router(self.router)
        self.app.on_startup(self.sockets.start_server)
        self.ui.run(title='Meridium Web App')
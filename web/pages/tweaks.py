from pages import message
from styling import theme

from nicegui import ui

def content(ui, app, sockets) -> None:
    with theme.frame('- Tweaks -'):
        ui.label('Tweaks!')
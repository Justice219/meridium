from pages import message
import styling as theme

from nicegui import ui

def content(ui, app, sockets) -> None:
    with theme.frame('- Tweaks -'):
        message('Tweaks!')
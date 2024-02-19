import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.message import message
from styling import theme

from nicegui import ui

def content(ui, app, sockets) -> None:
    with theme.frame('- Home -'):
        message('Welcome!')
        # information paragraph
        ui.label('This is the home page of the Meridium Web App.').classes('text-white-8')
        ui.label("To get started, please select an option from the menu.").classes('text-white-8')
        # menu
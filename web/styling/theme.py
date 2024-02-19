from contextlib import contextmanager
from components.menu import *

from nicegui import ui


@contextmanager
def frame(navtitle: str):
    ui.colors(primary='#1a1919', secondary='#242424', accent='#242424', positive='#242424')
    ui.query('body').style('background-color: #242424')
    # text color
    ui.query('body').style('color: #ffffff')

    with ui.header().classes('justify-between text-white'):
        ui.label('Meridium Web App 1.0').classes('font-bold')
        ui.label(navtitle)
        with ui.row():
            menu()
    with ui.column().classes('absolute-center items-center '):
        yield
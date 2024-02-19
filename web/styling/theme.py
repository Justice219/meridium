from contextlib import contextmanager
from components.menu import *

from nicegui import ui


@contextmanager
def frame(navtitle: str):
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
    ui.colors(primary='#1a1919', secondary='#242424', accent='#242424', positive='#00ff00')
    ui.query('body').style('background-color: #242424')
    # text color
    ui.query('body').style('color: #ffffff')

    with ui.header().classes('justify-between text-white'):
        ui.label('Meridium Web App 1.1').classes('font-bold')
        ui.label(navtitle)
        with ui.row():
            menu()

    yield

    # footer with github link
    with ui.footer().classes('justify-center text-white'):
        with ui.row().classes("justify-center items-center"):
            ui.label('Developed by Justice219').style('font-weight: bold;')

            # open github url
            ui.button(on_click=lambda: ui.open("https://github.com/Justice219/meridium", new_tab=True)).style('border: none; background: none;').classes('eva eva-github text-3xl').style('position: absolute; right: 0; padding-right: 20px; width: 1%; height: 1%;')


@contextmanager
def box(title, style=None):
    # Apply default styles and merge with any provided styles
    default_style = {
        'padding': '10px',
        'margin': '10px',
        'border': '1px solid #34495E',
        'border-radius': '5px',
        'background-color': '#242424',
        'box-sizing': 'border-box',
        'display': 'flex',
        'flex-direction': 'column',  # Stack children vertically
        'align-items': 'stretch',  # Stretch children to fill the width of the box
        'min-height': '200px',
        'flex': '1',  # Allow the box to grow to fill available space
        'min-width': '0',  # Allows the box to shrink below its minimum content size if necessary
    }
    
    if style:
        final_style = {**default_style, **style}  # Override default styles with any provided styles
    else:
        final_style = default_style

    final_style_string = '; '.join(f"{key}: {value}" for key, value in final_style.items())

    with ui.card().style(final_style_string):
        if title:
            ui.label(title).classes('text-white').style('font-weight: bold; margin-bottom: 10px;')
        yield
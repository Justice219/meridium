from styling import theme
from nicegui import ui

options = {
    "browsers": False,
    "spotify": False,
    "discord": False,
    "windows": False
}

async def confirm(sockets):
    with ui.dialog() as dialog, ui.card().style('background-color: #242424; color: #ffffff; border: none;'):
        ui.label('Are you sure you want to clean temporary files?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit("Yes"))
            ui.button('No', on_click=lambda: dialog.submit("No"))

    result = await dialog
    if result == "Yes":
        # Create table of only true options
        data = []
        for key, value in options.items():
            if value == True:
                data.append(key)

        # Use sockets to send options to desktop app
        ui.notify("Cleaned temporary files!", type="positive")
        await sockets.send_message("cleanTempFiles - " + str(data))

    else:
        ui.notify("Cancelled")

def update_option(key, value):
    # for some reason we get the actual checkbox object instead of the value 
    # i could fix it but what type of programmer would i be if i didn't just do this
    options[key] = value.value

def content(ui, app, sockets) -> None:
    with theme.frame('- Clean -'):
        # Clean temporary files button
        with ui.row():
            ui.button('Clean temporary files', on_click=lambda: confirm(sockets))
        
        # Define checkbox callback with specific option key
        def checkbox_callback(key):
            return lambda value: update_option(key, value)

        # Setup checkboxes with callbacks
        with ui.row():
            ui.checkbox('Browsers', on_change=checkbox_callback('browsers'))
            ui.checkbox("Spotify", on_change=checkbox_callback('spotify'))
            ui.checkbox("Discord", on_change=checkbox_callback('discord'))
            ui.checkbox("Windows", on_change=checkbox_callback('windows'))

        ui.label('Cleans temporary files from selected options to clear up space.').classes('text-white-8')

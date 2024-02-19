from styling import theme
from nicegui import ui

options = {
    "browsers": False,
    "spotify": False,
    "discord": False,
    "windows": False
}

async def clean_temp_files(sockets):
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

async def clean_cache_files(sockets):
    with ui.dialog() as dialog, ui.card().style('background-color: #242424; color: #ffffff; border: none;'):
        ui.label('Are you sure you want to clean cache files?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit("Yes"))
            ui.button('No', on_click=lambda: dialog.submit("No"))

    result = await dialog
    if result == "Yes":
        # Use sockets to send options to desktop app
        ui.notify("Cleaned cache files!", type="positive")
        await sockets.send_message("cleanCacheFiles")
    else:
        ui.notify("Cancelled")

async def empty_recycle_bin(sockets):
    with ui.dialog() as dialog, ui.card().style('background-color: #242424; color: #ffffff; border: none;'):
        ui.label('Are you sure you want to empty the recycle bin?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit("Yes"))
            ui.button('No', on_click=lambda: dialog.submit("No"))

    result = await dialog
    if result == "Yes":
        # Use sockets to send options to desktop app
        ui.notify("Emptied recycle bin!", type="positive")
        await sockets.send_message("emptyRecycleBin")
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
            ui.button('Clean temporary files', on_click=lambda: clean_temp_files(sockets))
        
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

        # break line    
        ui.html('<br>')

        # clean cache files
        with ui.row():
            ui.button('Clean cache files', on_click=lambda: clean_cache_files(sockets))

        ui.label('Cleans cache files to clear up space.').classes('text-white-8')
        ui.label('Note: This may delete certain important files.').classes('text-white-8')

        # break line
        ui.html('<br>')

        # clean recycle bin
        with ui.row():
            ui.button('Empty recycle bin', on_click=lambda: empty_recycle_bin(sockets))

        ui.label('Empties the recycle bin to clear up space.').classes('text-white-8')
        ui.label('Note: This may delete important files.').classes('text-white-8')



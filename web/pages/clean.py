from styling import theme
from nicegui import ui

options = {
    "browsers": False,
    "spotify": False,
    "discord": False,
    "windows": False
}
browser_options = {
    "cookies": False,
    "cache": False,
    "history": False,
    "siteData": False
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

async def clean_recycle_bin(sockets):
    with ui.dialog() as dialog, ui.card().style('background-color: #242424; color: #ffffff; border: none;'):
        ui.label('Are you sure you want to clean the recycle bin?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit("Yes"))
            ui.button('No', on_click=lambda: dialog.submit("No"))

    result = await dialog
    if result == "Yes":
        # Use sockets to send options to desktop app
        ui.notify("Cleaned recycle bin!", type="positive")
        await sockets.send_message("cleanRecycleBin")
    else:
        ui.notify("Cancelled")

async def clean_browser_data(sockets):
    with ui.dialog() as dialog, ui.card().style('background-color: #242424; color: #ffffff; border: none;'):
        ui.label('Are you sure you want to clean browser data?')
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit("Yes"))
            ui.button('No', on_click=lambda: dialog.submit("No"))

    result = await dialog
    if result == "Yes":
        # Create table of only true options
        data = []
        for key, value in browser_options.items():
            if value == True:
                data.append(key)

        # Use sockets to send options to desktop app
        ui.notify("Cleaned browser data!", type="positive")
        await sockets.send_message("cleanBrowserData - " + str(data))
    else:
        ui.notify("Cancelled")

def update_option(table, key, value):
    # for some reason we get the actual checkbox object instead of the value 
    # i could fix it but what type of programmer would i be if i didn't just do this
    table[key] = value.value

def content(ui, app, sockets) -> None:
    # Define checkbox callback with specific option key
    def checkbox_callback(table, key):
        return lambda value: update_option(table, key, value)

    with ui.column().style('display: flex; flex-direction: column; height: 100vh;'):

        # Flex container for boxes, ensuring they wrap and are spaced evenly
        with theme.frame('Clean System Tools'):
            # Flex container for boxes, ensuring they wrap and are spaced evenly
            with ui.column().style('flex: 1; overflow-y: auto;'):
                with ui.row().classes('flex-wrap').style('display: flex; justify-content: space-around; align-items: stretch;'):

                    # Common box style, ensuring equal width and starting at the same minimum height
                    box_style = {
                        'padding': '10px',
                        'margin': '0px',
                        'border': '1px solid #34495E',
                        'border-radius': '5px',
                        'background-color': '#242424',
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'stretch',
                        'flex': '1',
                        'min-width': '500px',  # Allows the box to shrink if needed
                        'min-height': '200px',
                        'box-sizing': 'border-box', 
                    }

                    # Temporary Files box
                    with theme.box('Temporary Files', style=box_style):
                        ui.label('Select the applications to clean temporary files from:').classes('text-white-8').style('margin-bottom: 10px;')
                        with ui.row().style('display: flex; justify-content: space-around;'):
                            ui.checkbox('Browsers', on_change=checkbox_callback(options, 'browsers')).style('flex: 1;')
                            ui.checkbox("Spotify", on_change=checkbox_callback(options, 'spotify')).style('flex: 1;')
                            ui.checkbox("Discord", on_change=checkbox_callback(options, 'discord')).style('flex: 1;')
                            ui.checkbox("Windows", on_change=checkbox_callback(options, 'windows')).style('flex: 1;')
                        ui.button('Clean Temporary Files', on_click=lambda: clean_temp_files(sockets)).style('width: 100%; margin-top: 10px;')

                    # Cache Files box
                    with theme.box('Cache Files', style=box_style):
                        ui.label('Clean cache files to free up space.').classes('text-white-8')
                        ui.label('Note: This may delete certain important files.').classes('text-white-8').style('font-size: 12px; margin-bottom: 42px;')
                        ui.button('Clean Cache Files', on_click=lambda: clean_cache_files(sockets)).style('width: 100%;')

                    # Recycle Bin box
                    with theme.box('Recycle Bin', style=box_style):
                        ui.label('Empty the recycle bin to clear up space.').classes('text-white-8')
                        ui.label('Note: This action is irreversible.').classes('text-warning').style('font-size: 12px; margin-bottom: 32px;')

                        with ui.row().style('display: flex; justify-content: space-around;'):
                            ui.button('Empty Recycle Bin', on_click=lambda: empty_recycle_bin(sockets)).style('width: 100%; margin-top: 10px; position: relative; bottom: 0;')
                        

                    # Browser Data box
                    with theme.box('Browser Data', style=box_style):
                        ui.label('Select browser data to clean:').classes('text-white-8').style('margin-bottom: 10px;')
                        with ui.row().style('display: flex; justify-content: space-around;'):
                            ui.checkbox('Cookies', on_change=checkbox_callback(browser_options, 'cookies')).style('flex: 1;')
                            ui.checkbox("Cache", on_change=checkbox_callback(browser_options, 'cache')).style('flex: 1;')
                            ui.checkbox("History", on_change=checkbox_callback(browser_options, 'history')).style('flex: 1;')
                            ui.checkbox("Site Data", on_change=checkbox_callback(browser_options, 'siteData')).style('flex: 1;')
                        ui.button('Clean Browser Data', on_click=lambda: clean_browser_data(sockets)).style('width: 100%; margin-top: 10px;')

                    # empty box to fill space
                    with theme.box('', style=box_style):
                        ui.label('')

                    # empty box to fill space
                    with theme.box('', style=box_style):
                        ui.label('')
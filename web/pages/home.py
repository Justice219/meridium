import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.message import message
from styling import theme

from nicegui import ui

def content(ui, app, sockets) -> None:
    with theme.frame('- Home -'):
        with ui.card().style('background-color: #242424; color: #ffffff; border: none; width: 150%; hei') as card:
            # header
            ui.label('Welcome to Meridium!').style('font-size: 24px; font-weight: bold;')
            
            ui.html('''
            <p>
                Meridium is a web app that allows you to control your desktop from your browser!
                You can do things like clean your recycle bin, clean your browser data, and more!
                Meridium is a work in progress and is being developed by <a href="https://github.com/Justice219/meridium" style="color: #f23a3a;">Justice219</a>
                    </p>
            ''').style('font-size: 16px;')

            ui.html('''
            <p> 
                Meridium uses websockets to communicate with a <span style="color: #e8234a;">desktop subprocess</span>, which controls the desktop.
                This project was an experiment to learn how to use <span style="color: #e8234a;">websockets</span>, and create a server/client application.
                The desktop subprocess is written in Python, and the web app is written in Python using the NiceGUI package.
                <br></br>
                This project may not be the most <span style="color: #e8234a;">SECURE</span>, and is not recommended for use in a production environment.
                However, it does work as intended, and is a fun project to play around with!
                
            </p>
            ''').style('font-size: 16px;')

            ui.label('Features:').style('font-size: 20px; font-weight: bold;')
            
            # Define a consistent card style
            card_style = 'background-color: #242424; color: #ffffff; border: none; margin: 10px; display: flex; flex-direction: column; flex: 1; width: 300px;'
            
            # Adjust row style for flex layout
            row_style = 'display: flex; justify-content: space-around; flex-wrap: wrap;'
            
            # Use a row with flex layout to evenly distribute the cards
            with ui.row().style(row_style):
                # Define each feature card
                feature_cards = [
                    ("Clean Temporary Files", ["Browsers", "Spotify", "Discord", "Windows"]),
                    ("Clean Cache Files", ["Cleans cache files to clear up space."]),
                    ("Empty Recycle Bin", []),
                    ("Clean Browser Data", ["Cache", "Cookies", "History", "Site Data"]),
                    ("Registry Tweaks", ["Coming soon!"]),
                    ("Uninstall Bloatware", ["Coming soon!"])
                ]
                
                # Create cards for each feature
                for title, items in feature_cards:
                    with ui.card().style(card_style):
                        ui.label(title).style('font-size: 18px; font-weight: bold;')
                        for item in items:
                            ui.label(item).style('font-size: 16px;')
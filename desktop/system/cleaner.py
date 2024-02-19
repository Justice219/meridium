import os
import shutil
import asyncio
import winreg as reg
import psutil

from system.process_util import process_open, close_application

class Cleaner():
    def __init__(self, sockets):
        self.name = "Cleaner"
        self.sockets = sockets

    async def check_and_close_applications(self, applications: list[str]):
        for application in applications:
            if await process_open(application):
                print(f"CLIENT: {application.capitalize()} is open. Attempting to close.")
                await close_application(application)
                print(f"CLIENT: {application.capitalize()} has been closed.")

    async def find_installed_browser(self):
        browsers = {
            "chrome": r"Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
            "firefox": r"Software\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe",
            "edge": r"Software\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
            "opera": r"Software\Microsoft\Windows\CurrentVersion\App Paths\opera.exe",
        }
        installed_browsers = []
        for browser, reg_path in browsers.items():
            try:
                # Attempt to open the registry key. This key exists if the browser is installed.
                with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path, 0, reg.KEY_READ) as key:
                    # If the key exists, append the browser to the list of installed browsers
                    installed_browsers.append(browser)
                    print(f"CLIENT: {browser.capitalize()} is installed")
            except FileNotFoundError:
                # If the key does not exist, the browser is not installed.
                pass
        return installed_browsers
    
    async def clean_temp_files(self, message: str):
        # Define application paths
        application_paths = {
            "spotify": os.path.expanduser('~\\AppData\\Local\\Spotify\\Storage'),
            "discord": os.path.expanduser('~\\AppData\\Roaming\\Discord\\Cache'),
            "windows": os.getenv('TEMP'),
        }
        # Define browser cache locations
        browser_cache_paths = {
            "chrome": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
            "firefox": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
            "edge": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
            "opera": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Cache'),
        }
        
        # Initialize an empty list for applications to clean
        applications_to_clean = []

        # Check for explicit application mentions in the message and add them to the list
        for app in application_paths.keys():
            if app in message.lower():
                applications_to_clean.append(app)

        # Clean mentioned applications
        await self.check_and_close_applications(applications_to_clean)
        for application in applications_to_clean:
            path = application_paths.get(application)
            if path and os.path.exists(path):
                try:
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"CLIENT: Cleaned {application.capitalize()} temp files in {path}")
                except Exception as e:
                    print(f"CLIENT: Error cleaning {application.capitalize()} temp files in {path}: {e}")

        # Separate handling for browsers if 'browsers' is mentioned
        if "browsers" in message.lower():
            installed_browsers = await self.find_installed_browser()
            for browser in installed_browsers:
                browser_path = browser_cache_paths.get(browser)
                if browser_path and os.path.exists(browser_path):
                    try:
                        await self.check_and_close_applications([browser])
                        shutil.rmtree(browser_path, ignore_errors=True)
                        print(f"CLIENT: Cleaned {browser.capitalize()} temp files in {browser_path}")
                    except Exception as e:
                        print(f"CLIENT: Error cleaning {browser.capitalize()} temp files in {browser_path}: {e}")

        # send a message to web app that the cleaning is done so it can display a notification
        await self.sockets.send_message("Sucess - Cleaned temporary files")

    async def clean_cache_files(self):
        # Define cache paths
        cache_paths = {
            # application related cache
            "spotify": os.path.expanduser('~\\AppData\\Local\\Spotify\\Storage'),
            "discord": os.path.expanduser('~\\AppData\\Roaming\\Discord\\Cache'),
            "teams": os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Teams\\Cache'),
            "slack": os.path.expanduser('~\\AppData\\Local\\slack\\Cache'),
            "zoom": os.path.expanduser('~\\AppData\\Roaming\\Zoom\\bin\\Cache'),
            "skype": os.path.expanduser('~\\AppData\\Local\\Packages\\Microsoft.SkypeApp_kzf8qxf38zg5c\\LocalState\\Cache'),
            "whatsapp": os.path.expanduser('~\\AppData\\Local\\WhatsApp\\Cache'),
            "telegram": os.path.expanduser('~\\AppData\\Roaming\\Telegram Desktop\\Cache'),
            "signal": os.path.expanduser('~\\AppData\\Roaming\\Signal\\app\\cache'),

            # browser related cache
            "chrome": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
            "firefox": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
            "edge": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
            "opera": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Cache'),
           
            # windows related cache
            "windows": os.getenv('TEMP'),
            "thumbnail": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Explorer'),
            "update": os.path.expanduser('~\\Windows\\SoftwareDistribution\\Download'),
            "office": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Office\\16.0\\OfficeFileCache'),
            "store": os.path.expanduser('~\\AppData\\Local\\Packages\\Microsoft.WindowsStore_8wekyb3d8bbwe\\LocalState\\Cache'),
            
            # adobe related cache
            "adobe": os.path.expanduser('~\\AppData\\Local\\Adobe\\OOBE'),
            "premiere": os.path.expanduser('~\\AppData\\Local\\Adobe\\Common\\Media Cache Files'),
            "after_effects": os.path.expanduser('~\\AppData\\Roaming\\Adobe\\Common\\Media Cache Files'),
            "photoshop": os.path.expanduser('~\\AppData\\Local\\Adobe\\Adobe Photoshop 2021\\Adobe Photoshop 2021 Settings\\Temp'),
            "illustrator": os.path.expanduser('~\\AppData\\Local\\Adobe\\Adobe Illustrator 25 Settings\\en_US\\AIPrefs'),
            "lightroom": os.path.expanduser('~\\AppData\\Local\\Adobe\\Lightroom\\Cache'),
            "acrobat": os.path.expanduser('~\\AppData\\Local\\Adobe\\Acrobat\\DC\\Cache'),
            "bridge": os.path.expanduser('~\\AppData\\Roaming\\Adobe\\Bridge CC\\Cache'),
            "indesign": os.path.expanduser('~\\AppData\\Local\\Adobe\\InDesign\\Version 16.0\\Caches'),
            "media_encoder": os.path.expanduser('~\\AppData\\Roaming\\Adobe\\Common\\Media Cache'),
            "prelude": os.path.expanduser('~\\AppData\\Roaming\\Adobe\\Common\\Media Cache Files'),

            # apple related cache
            "apple": os.path.expanduser('~\\AppData\\Local\\Apple Computer\\MobileSync\\Backup'),
            "itunes": os.path.expanduser('~\\AppData\\Local\\Apple Computer\\iTunes\\iPad Software Updates'),
            "quicktime": os.path.expanduser('~\\AppData\\Local\\Apple Computer\\QuickTime\\Downloads'),
            "safari": os.path.expanduser('~\\AppData\\Local\\Apple Computer\\Safari'),
            "icloud": os.path.expanduser('~\\AppData\\Local\\Apple Computer\\iCloud\\Photos\\Downloads'),

            # game stores cache
            "steam": os.path.expanduser('~\\AppData\\Local\\Steam\\htmlcache'),
            "epic": os.path.expanduser('~\\AppData\\Local\\EpicGamesLauncher\\Saved\\Logs'),
            "origin": os.path.expanduser('~\\AppData\\Local\\Origin\\Cache'),
            "uplay": os.path.expanduser('~\\AppData\\Local\\Ubisoft Game Launcher\\cache'),
            "gog": os.path.expanduser('~\\AppData\\Local\\GOG.com\\Galaxy\\webcache'),
            "battle_net": os.path.expanduser('~\\AppData\\Local\\Battle.net\\Cache'),
            "minecraft": os.path.expanduser('~\\AppData\\Roaming\\.minecraft\\logs'),
            "rockstar": os.path.expanduser('~\\AppData\\Local\\Rockstar Games\\Launcher\\logs'),

            # virus scanners cache
            "avast": os.path.expanduser('~\\AppData\\Local\\AVAST Software\\Avast\\log'),
            "avg": os.path.expanduser('~\\AppData\\Local\\AVG\\log'),
            "bitdefender": os.path.expanduser('~\\AppData\\Local\\Bitdefender\\log'),
            "kaspersky": os.path.expanduser('~\\AppData\\Local\\Kaspersky Lab\\log'),
            "norton": os.path.expanduser('~\\AppData\\Local\\Norton\\log'),
            "mcafee": os.path.expanduser('~\\AppData\\Local\\McAfee\\log'),
            "eset": os.path.expanduser('~\\AppData\\Local\\ESET\\log'),
            "avira": os.path.expanduser('~\\AppData\\Local\\Avira\\log'),
            "sophos": os.path.expanduser('~\\AppData\\Local\\Sophos\\log'),
            "malwarebytes": os.path.expanduser('~\\AppData\\Local\\Malwarebytes\\log'),
            "adaware": os.path.expanduser('~\\AppData\\Local\\Adaware\\log'),
        }

        # Clean cache files
        for path in cache_paths.values():
            if path and os.path.exists(path):
                print(f"CLIENT: Found cache files in {path}, attempting to clean!")
                try:
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"CLIENT: Cleaned cache files in {path}")
                except Exception as e:
                    print(f"CLIENT: Error cleaning cache files in {path}: {e}")

        # send a message to web app that the cleaning is done so it can display a notification
        await self.sockets.send_message("Sucess - Cleaned cache files")


# Example usage
#async def main():
#    cleaner = Cleaner()
#    applications_to_clean = ["spotify", "windows", "discord"]
#    await cleaner.clean_temp_files(applications_to_clean)

# Run the async main function
#asyncio.run(main())

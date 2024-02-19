import os
import shutil
import asyncio
import winreg as reg
import psutil
import win32com.client
import ctypes

from system.process_util import process_open, close_application

class Cleaner():
    def __init__(self, sockets):
        self.name = "Cleaner"
        self.sockets = sockets

    async def directory_size(self, path):
        """Calculate the total size of files in a given directory."""
        total_size = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                filepath = os.path.join(root, f)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size

    async def clean_directory(self, path):
        """Calculate the size before and after cleaning a directory, then remove the directory."""
        initial_size = await self.directory_size(path)
        shutil.rmtree(path, ignore_errors=True)
        final_size = await self.directory_size(path)  # Should be 0 if everything is deleted
        freed_size = initial_size - final_size
        return freed_size

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
            "operagx": r"Software\Microsoft\Windows\CurrentVersion\App Paths\opera_gx.exe",
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
                # If the key does not exist, try and find the exe in AppData/Local/Programs/browser-name
                try:
                    # Get the path to the browser's exe
                    path = os.path.expanduser(f'~\\AppData\\Local\\Programs\\{browser}\\{browser}.exe')
                    if os.path.exists(path):
                        installed_browsers.append(browser)
                        print(f"CLIENT: {browser.capitalize()} is installed")
                except FileNotFoundError:
                    print(f"CLIENT: {browser.capitalize()} is not installed")
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
            "operagx": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera GX Stable\\Cache'),
        }
        
        total_freed = 0  # Initialize total freed storage counter
        applications_to_clean = [app for app in application_paths if app in message.lower()]

        await self.check_and_close_applications(applications_to_clean)
        for application in applications_to_clean:
            path = application_paths.get(application, "")
            if path and os.path.exists(path):
                try:
                    freed_size = await self.clean_directory(path)
                    total_freed += freed_size
                    print(f"CLIENT: Cleaned {application.capitalize()} temp files in {path}, freed {freed_size} bytes - mb: {freed_size / 1024 / 1024}")
                except Exception as e:
                    print(f"CLIENT: Error cleaning {application.capitalize()} temp files: {e}")

        if "browsers" in message.lower():
            installed_browsers = await self.find_installed_browser()
            for browser in installed_browsers:
                path = browser_cache_paths.get(browser, "")
                if path and os.path.exists(path):
                    try:
                        await self.check_and_close_applications([browser])
                        freed_size = await self.clean_directory(path)
                        total_freed += freed_size
                        print(f"CLIENT: Cleaned {browser.capitalize()} cache in {path}, freed {freed_size} bytes - mb: {freed_size / 1024 / 1024}")
                    except Exception as e:
                        print(f"CLIENT: Error cleaning {browser.capitalize()} cache: {e}")

        print(f"Total storage freed: {total_freed} bytes")

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
        total_freed = 0
        for path in cache_paths.values():
            if path and os.path.exists(path):
                try:
                    freed_size = await self.clean_directory(path)
                    total_freed += freed_size
                    print(f"CLIENT: Cleaned cache files in {path}, freed {freed_size} bytes - mb: {freed_size / 1024 / 1024}")
                except Exception as e:
                    print(f"CLIENT: Error cleaning cache files: {e}")

        print(f"Total storage freed from cache: {total_freed} bytes")
        # Implement sending message via sockets here
        await self.sockets.send_message(f"Success - Cleaned cache files, freed {total_freed} bytes - mb: {total_freed / 1024 / 1024}")

    async def empty_recycle_bin(self):
        print("CLIENT: Attempting to empty recycle bin")
        try:
            # SHERB_NOCONFIRMATION = 0x00000001
            # SHERB_NOPROGRESSUI = 0x00000002
            # SHERB_NOSOUND = 0x00000004
            flags = 0x00000001 | 0x00000002 | 0x00000004
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
            print("CLIENT: Recycle bin emptied successfully")
            # Implement sending message via sockets here
            await self.sockets.send_message("Success - Recycle bin emptied successfully")
        except Exception as e:
            print(f"CLIENT: Failed to empty recycle bin: {e}")
            await self.sockets.send_message(f"Failure - Unable to empty recycle bin: {e}")

    async def clean_browser_data(self, message: str):
                # Already defined browser data paths
        browser_data_paths = {
            "chrome": {
                "cache": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
                "history": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'),
                "cookies": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'),
                "site_data": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Site Data')
            },
            "firefox": {
                "cache": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
                "history": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
                "cookies": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
                "site_data": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles')
            },
            "edge": {
                "cache": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
                "history": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History'),
                "cookies": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies'),
                "site_data": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Site Data')
            },
            "opera": {
                "cache": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Cache'),
                "history": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\History'),
                "cookies": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Cookies'),
                "site_data": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Site Data')
            },
            "operagx": {
                "cache": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera GX Stable\\Cache'),
                "history": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera GX Stable\\History'),
                "cookies": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera GX Stable\\Cookies'),
                "site_data": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera GX Stable\\Site Data')
            },
        }
        total_freed = 0  # Initialize total freed storage counter
        installed_browsers = await self.find_installed_browser()  # Check installed browsers

        for browser in installed_browsers:
            if browser in message.lower():  # Check if browser needs to be cleaned
                await self.check_and_close_applications([browser])  # Close browser before cleaning
                for data_type, path in browser_data_paths[browser].items():
                    if path and os.path.exists(path):
                        try:
                            freed_size = await self.clean_directory(path)
                            total_freed += freed_size
                            print(f"CLIENT: Cleaned {browser.capitalize()} {data_type} in {path}, freed {freed_size} bytes - mb: {freed_size / 1024 / 1024}")
                        except Exception as e:
                            print(f"CLIENT: Error cleaning {browser.capitalize()} {data_type}: {e}")

        print(f"Total storage freed by cleaning browser data: {total_freed} bytes - mb: {total_freed / 1024 / 1024}")
        # Implement sending message via sockets here
        await self.sockets.send_message(f"Success - Cleaned browser data, freed {total_freed} bytes - mb: {total_freed / 1024 / 1024}")


# Example usage
#async def main():
#    cleaner = Cleaner()
#    applications_to_clean = ["spotify", "windows", "discord"]
#    await cleaner.clean_temp_files(applications_to_clean)

# Run the async main function
#asyncio.run(main())

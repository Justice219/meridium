import os
import shutil
import asyncio
import winreg as reg
import psutil

from system.process_util import process_open, close_application

class Cleaner():
    def __init__(self):
        self.name = "Cleaner"

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
        # Initial applications dictionary without browsers
        applications = {
            "spotify": os.path.expanduser('~\\AppData\\Local\\Spotify\\Storage'),
            "discord": os.path.expanduser('~\\AppData\\Roaming\\Discord\\Cache'),
            "windows": os.getenv('TEMP'),
        }
        # Browser cache locations, might adjust based on the specific setup
        browser_cache_paths = {
            "chrome": os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
            "firefox": os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles'),
            "edge": os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
            "opera": os.path.expanduser('~\\AppData\\Local\\Opera Software\\Opera Stable\\Cache'),
        }
        
        # Check installed browsers first
        installed_browsers = await self.find_installed_browsers()
        for browser in installed_browsers:
            applications[browser] = browser_cache_paths[browser]

        # Determine which applications (including installed browsers) to clean
        applications_to_clean = [app for app in applications if app in message.lower() or app in installed_browsers]

        # Ensure mentioned applications are closed before cleaning
        await self.check_and_close_applications(applications_to_clean)

        print("CLIENT: Cleaning temporary files")
        for application in applications_to_clean:
            path = applications.get(application)
            if path and os.path.exists(path):
                try:
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"CLIENT: Cleaned {application.capitalize()} temp files in {path}")
                except Exception as e:
                    print(f"CLIENT: Error cleaning {application.capitalize()} temp files in {path}: {e}")



# Example usage
#async def main():
#    cleaner = Cleaner()
#    applications_to_clean = ["spotify", "windows", "discord"]
#    await cleaner.clean_temp_files(applications_to_clean)

# Run the async main function
#asyncio.run(main())

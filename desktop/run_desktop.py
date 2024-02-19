import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from meridium import MeridiumApp

async def main():
    desktop_app = MeridiumApp()
    await desktop_app.run()

asyncio.run(main())

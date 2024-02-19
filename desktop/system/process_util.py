import psutil

async def process_open(application: str):
    """Check if an application process is currently running."""
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == application:
            return True
    return False

async def close_application(application: str):
    """Attempt to close an application by killing its process."""
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == application:
            proc.kill()
            return True
    return False

async def get_application_memory_usage(application: str):
    """Get memory usage of an application."""
    for proc in psutil.process_iter(attrs=['name', 'memory_info']):
        if proc.info['name'] == application:
            return proc.info['memory_info'].rss
    return 0

async def get_application_cpu_usage(application: str):
    """Get CPU usage of an application."""
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] == application:
            return proc.cpu_percent()
    return 0

async def get_application_disk_usage(application: str):
    """Get disk usage of an application."""
    for proc in psutil.process_iter(attrs=['name', 'memory_info']):
        if proc.info['name'] == application:
            return proc.info['memory_info'].vms
    return 0

async def check_and_close_applications(self, applications: list[str]):
    """Ensure applications are closed before cleaning."""
    for application in applications:
        if await self.process_open(application):
            print(f"CLIENT: {application.capitalize()} is open. Attempting to close.")
            await self.close_application(application)
            print(f"CLIENT: {application.capitalize()} has been closed.")

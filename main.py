import os
import subprocess
import sys


desktop_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'desktop')
web_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')

# run desktop app
subprocess.Popen([sys.executable, os.path.join(desktop_path, 'run_desktop.py')])
# run web app
subprocess.Popen([sys.executable, os.path.join(web_path, 'run_web.py')])
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from web import WebApp

web_app = WebApp()
web_app.run()
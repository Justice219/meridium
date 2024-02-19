import os
import sys
import subprocess
import asyncio

class Cleaner():
    def __init__(self):
        self.name = "Cleaner"

    def clean(self):
        print(f"{self.name} is cleaning")

    def run(self):
        self.clean()

    def clean_temp_files(self, message: str):
        spotify = message.__contains__("spotify")
        windows = message.__contains__("windows")
        discord = message.__contains__("discord")
        windows = message.__contains__("windows")

import os
import configparser
import asyncio

import pyautogui
import pyperclip

pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

class Utils:
    def __init__(self):
        self.load_config()
        self.load_variables()

    def load_config(self):
        properties_path = Utils.join('properties', 'config.properties')

        self.properties = configparser.ConfigParser()
        self.properties.read(properties_path)

    def load_variables(self):
        self.rok_app = Utils.join('assets', self.properties['app']['app_folder'], 'rok_app.png')
        self.start_button = Utils.join('assets', self.properties['app']['app_folder'], 'start_button.png')

        self.rankings_button = Utils.join('assets', self.properties['rankings']['rankings_folder'], 'rankings_button.png')
        self.power_button = Utils.join('assets', self.properties['rankings']['rankings_folder'], 'power_button.png')
        self.more_info_button = Utils.join('assets', self.properties['rankings']['rankings_folder'], 'more_info_button.png')
        self.help_button = Utils.join('assets', self.properties['rankings']['rankings_folder'], 'help_button.png')

    def get_rok_app(self):
        return self.rok_app

    def get_start_button(self):
        return self.start_button

    def get_rankings_button(self):
        return self.rankings_button

    def get_power_button(self):
        return self.power_button

    def get_more_info_button(self):
        return self.more_info_button

    def get_help_button(self):
        return self.help_button

    @staticmethod
    def get_working_path():
        return os.path.dirname(__file__)

    @staticmethod
    def join(*args):
        path = Utils.get_working_path()

        for args in args:
            path = os.path.join(path, args)

        return path

    @staticmethod
    async def open_app():
        utils = Utils()

        if utils.click_start():
            return

        try:
            rok_app = pyautogui.locateOnScreen(utils.get_rok_app(), confidence=0.9)
            pyautogui.click(rok_app)
        except:
            return

        utils.click_start()

    def click_start(self):
        try:
            start_button = pyautogui.locateOnScreen(self.start_button, confidence=0.9)
            pyautogui.click(start_button)
            return True
        except:
            pass

        return False

    @staticmethod
    async def wait_app():
        await asyncio.sleep(15)
        pyautogui.click(x=1, y=1)
        await asyncio.sleep(15)

    @staticmethod
    def manual_click(a, b):
        pyautogui.click(x=a, y=b)

    @staticmethod
    async def get_rankings():
        utils = Utils()

        Utils.manual_click(50, 40)

        try:
            rankings_button = pyautogui.locateOnScreen(utils.get_rankings_button(), confidence=0.9)
            pyautogui.click(rankings_button)
        except:
            Utils.manual_click(519, 25)

            return

        try:
            power_button = pyautogui.locateOnScreen(utils.get_power_button(), confidence=0.9)
            pyautogui.click(power_button)
        except:
            Utils.manual_click(1455, 209)
            Utils.manual_click(519, 25)

            return

    @staticmethod
    def get_more_info():
        utils = Utils()
        
        utils.click_more_info()

    def click_more_info(self):
        try:
            more_info_button = pyautogui.locateOnScreen(self.more_info_button, confidence=0.9)
            pyautogui.click(more_info_button)
        except:
            pass

    @staticmethod
    def get_name():
        Utils.manual_click(1364, 371)
        return pyperclip.paste()

    @staticmethod
    async def close_app():
        pyautogui.hotkey('alt', 'f4')

    @staticmethod
    def get_kills_stats():
        utils = Utils()

        pyautogui.moveTo(913, 537)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        #utils.click_kills_stats()

    def click_kills_stats(self):
        try:
            help_button = pyautogui.locateOnScreen(self.help_button, confidence=0.9)
            pyautogui.click(help_button)
        except:
            pass
import pytesseract
import pyautogui
import numbers
import re
import configparser
import time

## pip install pytesseract
## pip install openpyxl

from PIL import Image
from openpyxl import Workbook

#from scan.Utils import Utils
#from scan.Rankings import Rankings
from Utils import Utils
from Rankings import Rankings

pyautogui.PAUSE = 1.5
pyautogui.FAILSAFE = True

_rankings = Rankings()

class DKP:
    def __init__(self):
        self.load_config()

    def load_config(self):
        properties_path = Utils.join('properties', 'dkp.properties')

        self.properties = configparser.ConfigParser()
        self.properties.read(properties_path)

    @staticmethod
    async def traverse_rankings(top):
        dkp = DKP()
        utils = Utils()

        wb = Workbook()
        ws = wb.active
        ws.append(['Rank', 'ID', 'Name', 'Power', 'Kill Points', 'Deaths', 'T4 Kills', 'T5 Kills'])

        file = Utils.join('data', f'{time.time()}.xlsx')

        w, h = pyautogui.size()
        h = 400

        ## Top 3
        for rank in range(1, 4):
            pyautogui.moveTo(w/2, h)
            pyautogui.click(x=w/2, y=h)

            id = dkp.get_id()
            name = utils.get_name()
            kp = dkp.get_kp()
            Utils.get_kills_stats()
            kills = DKP.get_kills()
            pyautogui.click(x=1, y=1)
            Utils.get_more_info()
            await DKP.get_dkp(rank, id, name, kp, kills, ws)

            Utils.manual_click(1456, 208)
            Utils.manual_click(1430, 250)

            h += 85

        for rank in range(4, (top + 1)):
            pyautogui.moveTo(w/2, 670)
            pyautogui.click(x=w/2, y=670)

            id = dkp.get_id()
            name = utils.get_name()
            kp = dkp.get_kp()
            Utils.get_kills_stats()
            kills = DKP.get_kills()
            pyautogui.click(x=1, y=1)
            Utils.get_more_info()
            await DKP.get_dkp(rank, id, name, kp, kills, ws)

            Utils.manual_click(1456, 208)
            Utils.manual_click(1430, 250)

        wb.save(file)

    def save_image(self, screenshot, name):
        image_file = Utils.join('assets', 'dkp', name)
        screenshot.save(image_file)

        return image_file

    def get_coordinates(self, section):
        coordinates = {}

        coordinates['x'] = int(self.properties[section]['x'])
        coordinates['y'] = int(self.properties[section]['y'])
        coordinates['w'] = int(self.properties[section]['w'])
        coordinates['h'] = int(self.properties[section]['h'])

        return coordinates

    @staticmethod
    async def get_dkp(rank, id, name, kp, kills, ws):
        dkp = DKP()

        power = dkp.get_power()
        deaths = dkp.get_deaths()
        if deaths == None or deaths == '':
            deaths = 0

        t4 = kills['t4']
        t5 = kills['t5']

        _rankings.add(rank, id, name, power, kp, deaths, t4, t5)
        ws.append([rank, id, name, f'{int(power):,}', f'{int(kp):,}', f'{int(deaths):,}', f'{int(t4):,}', f'{int(t5):,}'])

    def get_id(self):
        coordinates = self.get_coordinates('id')
        id = self.get(coordinates, 'id')
        return (re.sub(r'[^0-9]', '', id))

    def get_power(self):
        coordinates = self.get_coordinates('power')
        power = self.get(coordinates, 'power')
        return (re.sub(r'[^0-9]', '', power))

    def get_kp(self):
        coordinates = self.get_coordinates('kp')
        kp = self.get(coordinates, 'kp')
        return (re.sub(r'[^0-9]', '', kp))

    def get_deaths(self):
        coordinates = self.get_coordinates('deaths')
        deaths = self.get(coordinates, 'deaths')
        return (re.sub(r'[^0-9]', '', deaths))

    def get(self, coordinates, name):
        region = (coordinates['x'], coordinates['y'], coordinates['w'], coordinates['h'])
        screenshot = pyautogui.screenshot(region=region)

        saved_image = self.save_image(screenshot, f'{name}.png')
        image = Image.open(saved_image)

        value = pytesseract.image_to_string(image)
        return value

    @staticmethod
    async def get_ranking_id(id):
        return _rankings.get_id(id)

    @staticmethod
    async def get_ranking_rank(rank):
        return _rankings.get_rank(int(rank))

    @staticmethod
    def get_kills():
        dkp = DKP()

        _t4 = dkp.get_kills_count('t4')
        _t5 = dkp.get_kills_count('t5')

        if _t4 == None or _t4 == '':
            _t4 = 0
        if _t5 == None or _t5 == '':
            _t5 = 0

        t4 = int(int(_t4) / 10)
        t5 = int(int(_t5) / 20)

        kills = {
            't4' : t4,
            't5' : t5
        }

        return kills

    def get_kills_count(self, tier):
        coordinates = self.get_coordinates(tier)
        stats = self.get(coordinates, tier)
        return (re.sub(r'[^0-9]', '', stats))
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import urllib.request
import datetime
import os
import sys
sys.path.append(os.getcwd())
from Controller.Element import *
from Controller.ChromeController import ChromeController
from utils import *

PATH = os.getcwd()

class AutoFifa(ChromeController):
    def __init__(self, data, proxy_token, position):
        super().__init__()
        self.data = data
        self.proxy_token = proxy_token
        self.name_profile = f"acc_{data[0]}"  
        # self.id_profile = self.create_and_lauching_normal(name="tmp", position=position, token=self.proxy_token)
        self.id_profile = self.create_and_lauching_gologin(name=self.name_profile, position=position, token=self.proxy_token, path_profile = r"D:\testprofile")
        
    
    def login(self):

        self.driver.get("https://bilac.fconline.garena.vn/")
        time.sleep(2)
        self.do_click(by_locator=DANGNHAP, timewait=100)
        print("Đang nhập xong")
        sleep_short()
        self.do_sendkeys(by_locator=NHAPTAIKHOAN, timewait=5, text= self.data[1])
        sleep_very_short()
        self.do_sendkeys(by_locator=NHAPPASSWORD, timewait=5, text= self.data[2])
        sleep_very_short()
        self.do_click(by_locator=DANGNHAPNGAY, timewait=5)
    
    def do_event(self):
        sleep_long()
        self.do_click(by_locator=CHOIMIENPHI, timewait=100)
import requests
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
# import undetected_chromedriver as uc
# from seleniumwire import webdriver as webdriver_wire
# from PIL import Image
# from io import BytesIO
# from numpy import array
# import numpy as np
# from bs4 import BeautifulSoup
import re
import sys, os, pickle
from sys import platform
import random
import urllib.request
import json
sys.path.append(os.getcwd())
from Controller.gologin_offline.GologinController import GologinController
from Controller.ProxyController import *
from Controller.Element import *
from utils import *
# from CaptchaSolve.rotate_captcha import discern
# from CaptchaSolve.two_object_captcha import YoloCaptchaV2


from screeninfo import get_monitors

def get_pos(index):
    for m in get_monitors():
        if m.is_primary == True:
            num_x = m.width//300
            num_y = m.height//300 + 1
    x = index%num_x
    y = (index//num_x) if index//num_x <num_y else (index//num_x) // num_y
    return x*300, y*300

OMNI_API = 'http://localhost:35353'
PATH = os.getcwd()

class ChromeController:

    def __init__(self ):
        pass
    
    def create_and_lauching_normal(self, name, position, token):
        
        x, y = get_pos(index=position)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=300,400")
        options.add_argument(f"--window-position={x},{y}")
        options.add_argument("--disable-notifications")
        options.add_argument("--profile-directory=Default")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('disable-geolocation')
        options.add_argument('ignore-certificate-errors')
        options.add_argument('disable-popup-blocking')
        options.add_argument('disable-web-security')
        options.add_argument('disable-translate')
        options.add_argument('disable_capture')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option("detach", True)
            
        if token != '':
            tmproxy_resolver = ProxyController(token)
            myProxy = tmproxy_resolver.get_proxy()
            
            # print("myProxy:   ", myProxy)
        
            options.add_argument('--proxy-server=socks5://' + myProxy)

        self.driver = webdriver.Chrome(options=options)
        
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        
        # self.driver.get("https://iphey.com/")
        # self.driver.set_window_size(500,500)
        # self.driver.set_window_position(position[0],position[1])
        # try:
        #     self.driver.get(f'https://{position}')
        # except:
        #     pass
        return id
    
    def create_and_lauching_gologin(self, name, position, token, path_profile):
        x, y = get_pos(index=position)
        
        if token != '':
            tmproxy_resolver = ProxyController(api_key = token,use_proxy = 'https')
            myProxy = tmproxy_resolver.get_proxy()
        else:
            myProxy = ''
            
        if platform == "linux" or platform == "linux2":
            chrome_driver_path = PATH + "/Controller/gologin_offline/chromedriver"
        elif platform == "darwin":
            chrome_driver_path = PATH + "/Controller/gologin_offline/chromedriver"
        elif platform == "win32":
            chrome_driver_path = PATH + "/Controller/gologin_offline/chromedriver.exe"
            
        print("chrome_driver_path:            ", chrome_driver_path)
            
        self.g = GologinController(path_gologin="gologin", path_profile=path_profile)
        self.g.CreateProfile(name= name, proxy=myProxy)
        debugger_address = self.g.OpenProfile(port = 12000 + position)
        service = Service(executable_path=chrome_driver_path)
        
        options = webdriver.ChromeOptions()
        # options.add_argument("--window-size=300,300")
        # print("x, y:  ", x, y)
        # options.add_argument(f"--window-position={x},{y}")
        options.add_experimental_option("debuggerAddress", debugger_address)

        self.driver = webdriver.Chrome(options=options, service=service )
        self.driver.set_window_size(300,500)
        self.driver.set_window_position(x, y)
        # self.driver.get("https://pixelscan.net/")
        return self.driver
    
    def check_dialog(self):
        try:
            self.driver.switch_to.active_element
            element = self.driver.find_element(
                By.XPATH, '//div[@role="dialog"]')
            time.sleep(2)
            element.send_keys(Keys.ESCAPE)
            time.sleep(2)
            print('Bỏ qua dialog')
        except:
            return False
    
    def scroll_to_Element(self, by_locator):
        try:
            element = by_locator
            ActionChains(self.driver).scroll_to_element(element).perform()

        except:
            return False
    
    def do_click(self, by_locator, timewait):
        try:
            WebDriverWait(self.driver, timewait).until(
                EC.presence_of_element_located(by_locator)).click()
        except:
            return False
    
    def do_find_all_element_and_click(self, by_locator, index,  timewait):
        try:
            elm = WebDriverWait(self.driver, timewait).until(
                EC.presence_of_all_elements_located(by_locator))
            elm[index].click()
            return True
        except:
            return False
    
    def do_find_all_element_visibility_and_click(self, by_locator, index,  timewait):
        try:
            elm = WebDriverWait(self.driver, timewait).until(
                EC.visibility_of_element_located(by_locator))
            elm[index].click()
            return True
        except Exception as e:
            print("Lỗi : ", e)
            return False

    def do_sendkeys(self, by_locator, timewait, text):
        try:
            for t in text:
                WebDriverWait(self.driver, timewait).until(
                    EC.presence_of_element_located(by_locator)).send_keys(t)
                time.sleep(random.choice([0.05, 0.1, 0.15, 0.2]))
        except:
            return False
    def do_sendkey(self, by_locator, timewait, text):
        try:
            WebDriverWait(self.driver, timewait).until(
                EC.presence_of_element_located(by_locator)).send_keys(text)
        except:
            return False
            
    def do_select_by_index(self, by_locator, index):
        try:
            select = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(by_locator))
            # options = select.find_elements((By.XPATH, '//div[@role="option"]'))
            select[index].click()
        except:
            return False
    
    def do_select_by_text(self, by_locator, text):
        try:
            select = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(by_locator))
            option = select.find_element((By.XPATH, f'//div[contains( text( ), {text})]'))
            option.click()
        except:
            return False
    
    def do_find_element(self, by_locator, timewait):
        try:
            elm = WebDriverWait(self.driver, timewait).until(
                EC.presence_of_element_located(by_locator))
            return elm
        except:
            return False
    
    def do_find_element_visibility(self, by_locator, timewait):
        try:
            elm = WebDriverWait(self.driver, timewait).until(
                EC.visibility_of_element_located(by_locator))
            return elm
        except:
            return False
    
    def do_find_elements(self, by_locator, timewait):
        try:
            elms = WebDriverWait(self.driver, timewait).until(
                EC.presence_of_all_elements_located(by_locator))
            return elms
        except:
            return False
    
    def do_click_visibility(self, by_locator, timewait):
        try:
            WebDriverWait(self.driver, timewait).until(
                EC.visibility_of_element_located(by_locator)).click()
        except Exception as e:
            return False
    
    def check_text(self, text, time_wait):
        for _ in range(time_wait):
            if text in self.driver.find_element(By.TAG_NAME, "body").text:
                return True
            else:
                time.sleep(1)
        return False
    
    def download_img(self, by_locator, path):
        url = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(by_locator)).get_attribute("src")
        # url = self.driver.find_element(By.XPATH, by_locator).get_attribute("src")
        urllib.request.urlretrieve(url, path)
    
    def get_cookies(self):
        c = self.driver.get_cookies()
        pickle.dump(c, open("cookies.pkl", "wb"))
        cookies = ''
        for cookie in c:
            cookies += str(cookie) + ";"
        return cookies
    
    def load_cookies(self, cookies, url):
        cookies = cookies.replace("'", '"')
        cookies = cookies.replace("True", '"True"')
        cookies = cookies.replace("False", '"False"')
        cookies = cookies.split(";")
        cookies = cookies[:-1]
        cookies = [json.loads(t) for t in cookies]
        self.driver.get(url)
        for cookie in cookies:
            if cookie['httpOnly'] == "True":
                cookie['httpOnly'] = True
            elif cookie['httpOnly'] == "False":
                cookie['httpOnly'] = False
                
            if cookie['secure'] == "True":
                cookie['secure'] = True
            elif cookie['secure'] == "False":
                cookie['secure'] = False
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        
    
# -*- coding=utf-8 -*-
# !/usr/bin/env python
"""
Created on 25/09/2022

@author: Omnilogin | omnilog.in
"""
import json
import time
import traceback
import requests
from multiprocessing import Process, Event

from selenium import webdriver
from selenium.webdriver.common.by import By

OMNI_API = 'http://localhost:35353'


def main():

    omnilogin = Omnilogin()
    info = omnilogin.open_profile(profile_id=1)


class Omnilogin:

    def __init__(self, ):
        pass

    @staticmethod
    def open_profile(profile_id):
        for i in range(5):
            try:
                response = requests.get(f'{OMNI_API}/open?profile_id={profile_id}')
                print('Open profile code: ', response.status_code)
                if response.status_code != 200:
                    print(f'Open profile error {i}')
                    time.sleep(3)
                    continue
                body = response.json()
                if body.get('error'):
                    print(f'Open profile error {i}: {body.get("message")}')
                    time.sleep(3)
                    continue
                return body
            except Exception as e:
                traceback.print_exc()
                time.sleep(3)

    @staticmethod
    def create_profile(profile_name):
        info = {
            "name": profile_name,
            "account": {
                "platform": "gmail.com",
                "userDataType": "automatic"
            },
            "fingerprints": {
                "operating_system": "window",
                "ua_type": "Safe",
                "user_agent": "random",
                "timezone": True,
                "web_rtc": "automatic",  # "manual" | "real" | "disabled"
                "screen_resolution": "random",
                "fonts": "Custom",  # "SystemDefault"
                "canvas": "Noise",
                "web_gl_type": "Custom",
                "web_gl_image_type": "Noise",
                "audio_context": "Noise",
                "client_rects": "Noise",
                "lang": "",  # "random"
                "hardware_concurrency": 8
            },
            # Sử dụng embedded_proxy trong trường hợp muốn thêm proxy trực tiếp vào profle
            # "embedded_proxy": {
            #     "name": "Proxy us",
            #     "proxy_type": "HTTP",
            #     "host": "192.168.0.1",
            #     "port": 6969,
            #     "user_name": "",
            #     "password": ""
            # },
            # Sử dụng idProxy trong trường hợp đã thêm proxy trong phần quản lý proxy, ở đây chỉ cần điển lại proxy id
            # "idProxy": 0,
            "dest_url": [
                "https://whoer.net/"
            ],
            "group": {
                "id": "1"
            }
        }
        try:
            response = requests.post(f'{OMNI_API}/profiles', json=info)
            body = response.json()
            # print(f'Create profile "{profile_name}" success !!!')
            print("body : ", body)
            return body['id']
        except Exception as e:
            print(f'Create profile "{profile_name}" error with {e}')
            traceback.print_exc()
        return

    @staticmethod
    def delete_profile(profile_id):
        # deleteData: Pass 'y' to delete profile data folder. Other, not
        # deleteData: nếu muốn xóa cả folder profile thì là 'y', nếu không muốn xóa thì không điền gì cả
        response = requests.delete(f'{OMNI_API}/profiles/{profile_id}?deleteData=y')
        print(f'Delete profile {profile_id} ', response.content)

    @staticmethod
    def update_status(profile_id, status):
        response = requests.put(f'{OMNI_API}/profiles/{profile_id}/status', json={"status": status})
        print(f'Update status profile {profile_id} ', response.content)


class Gmail:

    def __init__(self, binary_location, debugger_address, executable_path):
        self.binary_location = binary_location
        self.debugger_address = debugger_address
        self.executable_path = executable_path

    def login_gmail(self):
        options = webdriver.ChromeOptions()
        options.binary_location = self.binary_location
        options.add_experimental_option("debuggerAddress", self.debugger_address)
        driver = webdriver.Chrome(executable_path=self.executable_path, options=options)
        driver.get('https://mail.google.com/mail/u/0/')
        time.sleep(5)
        try:
            driver.find_element(By.XPATH, '/html/body/header/div/div/div/a[2]').click()
            time.sleep(3)
        except Exception as e:
            pass
        try:
            driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys('khaitv96')
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="identifierNext"]').click()
        except Exception as e:
            pass
        time.sleep(5)
        # TODO: Get All Cookie
        all_cookies = driver.get_cookies()
        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        print("========== Cookies ========== \n", json.dumps(cookies_dict, indent=2))
        time.sleep(5)
        driver.close()


if __name__ == '__main__':
    main()

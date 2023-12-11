import time
from datetime import datetime

import requests


def is_past_time(time_string):
    current_time = datetime.now().time()
    target_time = datetime.strptime(time_string, "%H:%M:%S %d/%m/%Y").time()

    return current_time > target_time


import time
from datetime import datetime
from time import sleep
from requests import session
from urllib3 import disable_warnings , exceptions
import requests


def is_past_time(time_string):
    current_time = datetime.now().time()
    target_time = datetime.strptime(time_string, "%H:%M:%S %d/%m/%Y").time()

    return current_time > target_time


class ProxyController:
    def __init__(self, api_key, provider="tmproxy", use_proxy="socks5", new_proxy=True):
        self.api_key = api_key
        self.provider = provider
        self.use_proxy = use_proxy
        self.new_proxy = new_proxy
        
        self.session = session()
        self.session.verify = False
        self.session.trust_env = False
        
    def get_proxy(self):
        proxy , next_change = self.get_current_proxy()
        if proxy == 'error api key' or proxy == 'error_type_proxy':
            return 'error_check_api_key_again'
        else:
            # same ip: true => cho phép trùng ip => lấy proxy cũ khi chưa được đổi ip
            if self.new_proxy == False:
                if next_change == 0:
                    proxy , next_change = self.get_new_proxy()
                    return proxy
                else:
                    proxy, next_change = self.get_current_proxy()
                    return proxy
            else:
                
                # print("next_change:    ", type(next_change), next_change)
                # if next_change > 60:
                #     proxy , next_change = self.get_current_proxy()
                #     return proxy
                # else:
                for x in range(next_change):
                    print(f' => WAIT {next_change - x} FOR GET NEW PROXY',end='\r')
                    sleep(1)
                time.sleep(2)
                proxy , next_change = self.get_new_proxy()
                return proxy
                
    def get_current_proxy(self):
        api = f'https://tmproxy.com/api/proxy/get-current-proxy'
        playload = {"api_key": self.api_key}
        response = self.session.post(url=api , json=playload).json()
        if response['code'] != 0 and response['code'] != 27:
            # print(f'{self.api_key} => ERROR: {response}')
            return 'error api key' , 0
        else:
            data = response['data']
            ip_allow = data['ip_allow']
            location = data['location_name']
            socks5 = data['socks5']
            https = data['https']
            time_out = data['timeout']
            next_request = data['next_request']
            expired_at = data['expired_at']
            full_information = f'IP ALLOW: code: {response["code"]} {ip_allow}|LOCATION: {location}|SOCKS5: {socks5}|HTTP: {https}|TIME OUT: {time_out}|NEXT_REQUESTS: {next_request}|EXPIRED AT: {expired_at}'
            print(f'{self.api_key} get_current_proxy => FULL INFOR => {full_information}')
            if self.use_proxy == 'https':
                return https , next_request
            elif self.use_proxy == 'socks5':
                return socks5 , next_request
            else:
                print('{api_key} => ERROR TYPE PROXY - ONLY ACCEPT HTTP/SOCKS => [error: {type_proxy}]')
                return 'error_type_proxy' , 0
    
    def get_new_proxy(self):
        api = f'https://tmproxy.com/api/proxy/get-new-proxy'
        # 0 => random
        playload = {"api_key":self.api_key,"sign":"string","id_location":0}
        response = self.session.post(url=api , json=playload).json()
        data = response['data']
        ip_allow = data['ip_allow']
        location = data['location_name']
        socks5 = data['socks5']
        https = data['https']
        time_out = data['timeout']
        next_request = data['next_request']
        expired_at = data['expired_at']
        full_information = f'IP ALLOW: code: {response["code"]} {ip_allow}|LOCATION: {location}|SOCKS5: {socks5}|HTTP: {https}|TIME OUT: {time_out}|NEXT_REQUESTS: {next_request}|EXPIRED AT: {expired_at}'
        print(f'{self.api_key} get_new_proxy => FULL INFOR => {full_information}')
        
        if response["code"] == 5:
            time.sleep( 2)
            return self.get_proxy()
            
        if self.use_proxy == 'https':
            return https , next_request
        elif self.use_proxy == 'socks5':
            return socks5 , next_request
        else:
            return 'error_type_proxy'
        
class ProxyResolver:
    def __init__(self, api_key, provider="tmproxy", use_proxy="socks5"):
        self.api_key = api_key
        self.provider = provider
        self.use_proxy = use_proxy

    def get_proxy(self, ensure_new=False):
        try:
            data = {
                "api_key": self.api_key,
                "sign": "string",
                "id_location": 0
            }
            res = self.make_tmproxy_request("get-new-proxy", data)
            # print("res", res)
            if ensure_new:
                if res["code"] == 5:
                    print(
                        f"Proxy is not available, wait {res['data']['next_request']} seconds")
                    time.sleep(res['data']['next_request'] + 2)
                    return self.get_proxy()
            if res["code"] == 0:
                if res['data']["next_request"] < 30:
                    print(
                        f"Proxy is not available, wait {res['data']['next_request']} seconds")
                    time.sleep(res['data']['next_request'] + 2)
                    return self.get_proxy()
                else:
                    return res["data"][self.use_proxy]
            else:
                print("res code: ", res["code"])
                return self.get_current_proxy()
        except Exception as e:
            print(f"Error when get proxy by key {self.api_key}", e)
            return None

    def get_current_proxy(self):
        data = {
            "api_key": self.api_key
        }
        res = self.make_tmproxy_request("get-current-proxy", data)
        res_data = res["data"]
        # check expired_at time with the format "20:11:59 21/05/2023"
        if is_past_time(res_data['expired_at']):
            print("Current proxy expired, get new proxy")
            return self.get_proxy()

        return res["data"][self.use_proxy]

    def make_tmproxy_request(self, path, data):
        url = f"https://tmproxy.com/api/proxy/{path}"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        print("tmproxy res", response_json)

        return response_json


if __name__ == '__main__':
    while True:
        api_key = '6125c61ee19e988a6674d8c5ada10e0c'
        proxy = ProxyController(api_key=api_key)
        print(proxy.get_proxy())
        sleep(5)
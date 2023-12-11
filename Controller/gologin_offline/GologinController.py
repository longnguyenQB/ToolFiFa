import os, sys
import time
from sys import platform
from selenium import webdriver
# from gologin import getRandomPort
from selenium.webdriver.chrome.service import Service
sys.path.append(os.getcwd())
from Controller.gologin_offline.generator import GoLogin

PATH = os.getcwd()

def convert_path(path):
    path = path.replace("\a", "\\a")
    path = path.replace("\t", "\\t")
    path = path.replace("\r", "\\r")
    path = path.replace("\n", "\\n")
    path = path.replace("\f", "\\f")
    path = path.replace("\v", "\\v")
    path = path.replace("\b", "\\b")
    return path

class GologinController():
    def __init__(self, path_gologin, path_profile) -> None:
        self.path_profile = convert_path(path_profile)
        self.path_gologin = convert_path(path_gologin)
        self.Runing = GoLogin({
        "tmpdir": path_profile
    })
        if not os.path.exists(path_profile):
            os.makedirs(path_profile)
            
    def CreateProfile(self, name, proxy):
        if proxy != '':
            proxy = {
                        'mode': "http",
                        'host': proxy.split(":")[0],
                        'port': int(proxy.split(":")[1]),
                        'username': '',
                        'password': ''
                    }
        else:
            proxy = {
                        'mode': "none",
                        'host': '',
                        'port': None,
                        'username': '',
                        'password': ''
                    }
        
        print("proxy:            ", proxy)
        profile_id = self.Runing.create({
                                        "version": '116.0.5845.106',
                                        "os": 'win',
                                        "name": name,
                                        "proxy": proxy,
                                        "canvas": {
                                            "mode": 'noise'
                                        },
                                        "canvasMode": 'noise',
                                        "webRTC": {
                                            "mode": 'noise',
                                        },
                                        "webRtc": {
                                            "mode": 'noise',
                                        },
                                        "webGL": {
                                            "mode": 'noise',
                                        },
                                        "audioContext": {
                                            "mode": True,
                                        },
                                        "clientRects": {
                                            "mode": True,
                                        },

                                        "geoLocation": {
                                            "mode": 'noise',
                                        },
                                        "geolocation": {
                                            "mode": 'noise',
                                        },
                                        "googleServicesEnabled": True,
                                        "doNotTrack": True
                                    })
        self.Runing.setProfileId(profile_id)
        self.Runing.createStartup()
        if not profile_id:
            return
        profile = self.Runing.getProfile(profile_id)
        if profile:
            self.profile_id = profile_id
        else:
            return None



    def OpenProfile(self, port):
        self.RunProfile = GoLogin({
                            "profile_id": self.profile_id, # ID profile
                            "extra_params": ['--font-masking-mode=2'],
                            "folderBrowser": ".gologin", # Đường dẫn folder lưu browser và fonts
                            "tmpdir": self.path_profile # Đường dẫn lưu 
                            })
        
        try:
            debugger_address = self.RunProfile.start(port=port)
            return debugger_address
        except Exception as e:
            print('Erro Start', e)
            return False

        
    def End(self, driver, delete_profile):
        if delete_profile == True:
            driver.quit()
            self.RunProfile.stop()
            time.sleep(2)
            self.RunProfile.delete(profile_id=self.profile_id)
        else:
            driver.quit()
            self.RunProfile.stop()
        # RunProfile.stop()
        # RunProfile.delete(your_profile_id)


if __name__ == "__main__":
    path = convert_path("D:\testprofile")
    g = GologinController(path_gologin="gologin", path_profile=path, delete_profile=True)
    g.CreateProfile(proxy="")
    g.OpenProfile()
    g.End()
    # os.system(
    #     f'start C:\\Users\\s0ckd\\.gologin_test\\browser\\orbita-browser-114\\chrome.exe --user-data-dir=G:\\Temp\\64f10a6c3df4786648f7be5d '
    #     '--password-store=basic '
    #     '--donut-pie={test:test} '
    #     f"--font-masking-mode=2 "
    #     f"--disable-encryption "
    #     '--restore-last-session '
    #     )


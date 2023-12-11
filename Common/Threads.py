from PyQt5 import QtCore
from typing import List, Dict
import os
import sys
import subprocess
sys.path.append(os.getcwd())
from utils import *
from Controller.TiktokController import AutoFifa

PATH = os.getcwd()


class ThreadsFifa(QtCore.QThread):
    signal_data = QtCore.pyqtSignal(object)
    off_thread = QtCore.pyqtSignal(object, object)

    def __init__(self, data_row=List, proxy_token = str, thread_info=List):
        super(ThreadsFifa, self).__init__()
        self.data_row = data_row
        self.thread_info = thread_info
        self.is_running = True
        self.proxy_token = proxy_token

    def run(self):
        self.data_row[-1] = "Đang làm ..."
        self.signal_data.emit(self.data_row)
        self.auto = AutoFifa(data=self.data_row, 
                            proxy_token = self.proxy_token,
                            position = self.thread_info[0])
        self.auto.login()
        self.auto.do_event()
        self.auto.g.End(driver=self.auto.driver, delete_profile=True)
        self.data_row[-1] = "Đã làm xong!"
        self.signal_data.emit(self.data_row)
        
        self.off_thread.emit(self.thread_info[0], self.thread_info[1] + 1)

class ThreadsStop(QtCore.QThread):
    signal_data = QtCore.pyqtSignal(object)

    def __init__(self, 
                thread):
        
        super(ThreadsStop, self).__init__()
        self.thread = thread
        self.is_running = True

    def run(self):
        
        try:
            self.thread.stop()
            
        except Exception as e:
            print(e)
            

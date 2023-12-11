import win32gui
import win32process
import psutil
import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

def getProcessIDByName():
    pids = []
    process_name = "dnplayer.exe"

    for proc in psutil.process_iter():
        if process_name in proc.name():
            pids.append(proc.pid)

    return pids

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

def getWindowTitleByHandle(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def getWindownHandle(pid):
    tmp = []
    hwnds = get_hwnds_for_pid(pid)
    for hwnd in hwnds:
        if IsWindowVisible(hwnd):
            tmp.append(hwnd)
    return tmp

def winEnumHandler( hwnd, name_device ):
    if win32gui.IsWindowVisible( hwnd ):
        if win32gui.GetWindowText( hwnd ) == name_device:
            print("hwnd___________: ",hwnd)
            return hwnd
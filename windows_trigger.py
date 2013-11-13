import signal
import time
import os
import win32gui
import win32con
import win32process
import traceback
from subprocess import Popen


#==============================================================================
def write_parent_hwnd(hwnd, lParam):
    window_class = win32gui.GetClassName(hwnd)

    if win32gui.IsWindowVisible(hwnd):
        for cls in REQUIRED_CLASSES_PROGRAMS:
            if cls.lower() in window_class.lower():
                HWND_CLASS_LIST.append(hwnd)
    return True

#==============================================================================
if __name__ == '__main__':
    # Классы\путь к запускаемому файлу окон, по ним ищем hwnd окна\запускаем окно.
    REQUIRED_CLASSES_PROGRAMS = {'TkTopLevel': 'py -3 D:\WORK\sbis3\script\\test\\not_decided.pyw',
                                 'Chrome': '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --new-window chrome-extension://bpdhaofmkackpofgcippnjdkbgidkdnk/monitor.html',
                                 'Mozilla': '"C:\Program Files (x86)\Mozilla Firefox\\firefox.exe" http://dev-ci//plugin/jenkinswalldisplay/walldisplay.html?viewName=+++++++++++Platforma&jenkinsUrl=http%3A%2F%2Fdev-ci%2F'}
    TIMEOUT = 10
    HWND_CLASS_LIST = []  # Список hwnd(A handle to a window), по которым хотим переключаться.

    pid = os.getpid()
    win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0)  # Опция, позволяющая работать методу
                                                                             # SetForegroundWindow корректно,
                                                                             # если фокус с окна сбился.
    for prgm in REQUIRED_CLASSES_PROGRAMS.values():
        process = Popen(prgm)
        time.sleep(1)

    # Проходим по всем окнам.
    # Заполняем  словарь HWND_CLASS_LIST родительскими идентификаторами окон.
    win32gui.EnumWindows(write_parent_hwnd, 0)

    Popen('py -3 D:\WORK\sbis3\script\\test\\view_time_date.py')
    time.sleep(0.5)  # Без паузы сценарий не успевает полностью запуститься.
    CLOCK_HWND = win32gui.FindWindow(0, 'Clock')

    # Переключаем окна.
    while True:
        for hwnd in HWND_CLASS_LIST:
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.2)  # Без паузы не происходит последовательного перключения SetForegroundWindow().
            win32gui.SetForegroundWindow(CLOCK_HWND)
            time.sleep(TIMEOUT)
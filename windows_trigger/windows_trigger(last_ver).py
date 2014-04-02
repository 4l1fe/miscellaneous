import time
import os
import win32gui
import win32con
from subprocess import Popen


#=======вспомогательная функция, не используется==================================
def print_window_class_caption_hwnd(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        window_class = win32gui.GetClassName(hwnd)
        window_caption = win32gui.GetWindowText(hwnd)
        print('class = ', window_class, 'caption = ', window_caption, 'hwnd = ', hwnd)


#==============================================================================
def write_parent_hwnd(hwnd, lParam):
    window_class = win32gui.GetClassName(hwnd)

    if win32gui.IsWindowVisible(hwnd):
        for cls in REQUIRED_CLASSES:
            if cls.lower() in window_class.lower():
                HWND_CLASS_LIST.append(hwnd)
    return True

#==============================================================================
if __name__ == '__main__':
    # Классы\путь к запускаемому файлу окон, по ним ищем hwnd окна\запускаем окно.
    REQUIRED_CLASSES = ['TkTopLevel', 'Chrome', 'Mozilla']
    REQUIRED_PROGRAMS = ['py -3 C:\monitor\\not_decided.pyw',
                         '"C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window chrome-extension://khojaffakpmbndhfnnodlpggcmaodfoo/monitor.html',
                         '"C:\Program Files\Mozilla Firefox\\firefox.exe" http://dev-ci//plugin/jenkinswalldisplay/walldisplay.html?viewName=+++++++++++Platforma&jenkinsUrl=http%3A%2F%2Fdev-ci%2F',
                         'py -3 C:\monitor\\unrealized_tasks.py -cf "C:\monitor\list.csv" -ptm 600',
                         'py -3 C:\monitor\\generate_csv_file.py -s "C:\\Users\\dv.krasnov\\СБиС2\\sbis.exe" -prg "C:\\\monitor\\\Кол_воЗаданий.prg" -stm 600'
                         ]

    TIMEOUT = 60
    HWND_CLASS_LIST = []  # Список hwnd(A handle to a window), по которым хотим переключаться.

    pid = os.getpid()
    win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0)  # Опция, позволяющая работать методу
                                                                             # SetForegroundWindow корректно,
                                                                             # если фокус с окна сбился.
    for prgm in REQUIRED_PROGRAMS:
        process = Popen(prgm)
        time.sleep(2)

    # Проходим по всем окнам.
    # Заполняем  словарь HWND_CLASS_LIST родительскими идентификаторами окон.
    win32gui.EnumWindows(write_parent_hwnd, 0)

    Popen('py -3 C:\monitor\\view_time_date.py')
    time.sleep(2)  # Без паузы сценарий не успевает полностью запуститься.
    CLOCK_HWND = win32gui.FindWindow(0, 'Clock')

    # Переключаем окна.
    while True:
        for hwnd in HWND_CLASS_LIST:
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.4)  # Без паузы не происходит последовательного перключения SetForegroundWindow().
            win32gui.SetForegroundWindow(CLOCK_HWND)
            time.sleep(TIMEOUT)

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
    global DIALOG_HWND
    global CLOCK_HWND
    window_title = win32gui.GetWindowText(hwnd)
    window_class = win32gui.GetClassName(hwnd)

    # Ищем диалог, который вылазит при повисании BuildScreen
    if 'BuildScreen' in window_title and 'BuildScreen' not in window_class:
        print('Dialog', window_title)
        DIALOG_HWND = hwnd

    if 'Clock' in window_title:  # Никаких действий, если встретим окно со временем.
        pass
    elif win32gui.IsWindowVisible(hwnd):
        # Из всех окон нам нужны только REQUIRED_CLASSES.
        for cls in REQUIRED_CLASSES_PROGRAMS:
            if cls.lower() in window_class.lower() \
                and hwnd not in [elem[0] for elem in HWND_CLASS_LIST]:
                HWND_CLASS_LIST.append([hwnd, cls])
                WINDOW_IS_CLOSED[cls] = False
    return True


def check_window_condition(hwnd_class_list):
    global DIALOG_HWND
    if DIALOG_HWND:  # Если диалог появился, значит BuildScreen висит.
        # Сносим диалог
        tgreadid, pid = win32process.GetWindowThreadProcessId(DIALOG_HWND)
        print('pid dialog ', pid)
        os.kill(pid, signal.SIGTERM)

        for hwnd, cls in hwnd_class_list:
            if cls == 'BuildScreen':
                try:
                    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
                    os.kill(pid, signal.SIGTERM)
                    hwnd_class_list.remove([hwnd, cls])
                except OSError:
                    traceback.print_exc()
        WINDOW_IS_CLOSED['BuildScreen'] = True
        DIALOG_HWND = 0


#==============================================================================
if __name__ == '__main__':
    DIALOG_HWND = 0
    REQUIRED_CLASSES_PROGRAMS = {'TkTopLevel': 'py -3 D:\WORK\sbis3\script\\test\\not_decided.pyw',   # Классы\путь к запускаемому файлу окон, по ним ищем hwnd окна\запускаем окно.
                                 # 'Chrome': '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --kiosk http://dev-ci//plugin/jenkinswalldisplay/walldisplay.html?viewName=+++++++++++Platforma&jenkinsUrl=http%3A%2F%2Fdev-ci%2F',
                                 'Mozilla': '"C:\Program Files (x86)\Mozilla Firefox\\firefox.exe" http://dev-ci//plugin/jenkinswalldisplay/walldisplay.html?viewName=+++++++++++Platforma&jenkinsUrl=http%3A%2F%2Fdev-ci%2F',
                                 'BuildScreen': 'D:\download\BuildScreen\BuildScreen.exe'}
    WINDOW_IS_CLOSED = {cls: True for cls in REQUIRED_CLASSES_PROGRAMS}  # Генерация флагов существования окон требуемых окон.
    TIMEOUT = 5

    pid = os.getpid()
    win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0)  # Опция, позволяющая работать методу
                                                                             # SetForegroundWindow корректно,
                                                                             # если фокус с окна сбился.
    Popen('py -3 D:\WORK\sbis3\script\\test\\view_time_date.py')
    time.sleep(0.5)  # Без паузы сценарий не успевает полностью запуститься.
    CLOCK_HWND = win32gui.FindWindow(0, 'Clock')

    while True:
        HWND_CLASS_LIST = []  # Список hwnd(A handle to a window)\class окон, по которым хотим переключаться.

        # Проходим по всем окнам.
        # Заполняем  словарь HWND_CLASS_LIST родительскими идентификаторами окон.
        # Выставляем окнам флаг существования.
        win32gui.EnumWindows(write_parent_hwnd, 0)
        HWND_CLASS_LIST.sort(key=lambda elem: elem[1])  # Отсортируем по имени класса окна.
        print(HWND_CLASS_LIST)
        # Проверяем на отклик\завершаем процессы окон.
        check_window_condition(HWND_CLASS_LIST)

        # Открываем закрытые окна.
        for cls, prgm in REQUIRED_CLASSES_PROGRAMS.items():
            if WINDOW_IS_CLOSED[cls]:
                process = Popen(prgm)
                time.sleep(1)

        # Переключаем окна.
        for hwnd, cls in HWND_CLASS_LIST:
            try:
                if cls == 'BuildScreen':
                    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.2)  # Без паузы не происходит последовательного перключения SetForegroundWindow().
                win32gui.SetForegroundWindow(CLOCK_HWND)
            except Exception:
                print('except ', hwnd, cls)
                traceback.print_exc()
            time.sleep(TIMEOUT)
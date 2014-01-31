def OnEndAllLoadModules(answer):
    import subprocess
    import os
    import sbis


    switch_on = sbis.ConfigGet('ВключитьРоботаЭлектроннойПроходной')
    if switch_on.lower() == 'да':
        pid = os.getpid()
        onevent_file_path = os.path.abspath(os.path.dirname(__file__))
        cmd = 'py -3 robot.py -ppid {ppid}'.format(ppid=pid)
        startupinfo = subprocess.STARTUPINFO()  # Настройка для того, чтобы спрятать окно.
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        cwd = os.getcwd()

        # file = open(os.path.join(onevent_file_path, 'on_event_runtime_info.txt'), 'w')
        # file.write('pid = '+str(pid)+'\n')
        # file.write('onevent_file_path = '+onevent_file_path+'\n')
        # file.write('cwd = '+cwd)
        # file.close()

        subprocess.Popen(cmd, cwd=os.path.normpath(onevent_file_path), startupinfo=startupinfo)  # Запускаем из директории, где лежит сам robot.py,
                                                                                                                 # из-за бага в python 3.3.0 с запуском
                                                                                                                 # по абсолютному пути с русскими символвами
    return True


def OnCleanup(answer):
    return True


def OnCheckModules(answer):
    return True
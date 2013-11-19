import subprocess
import argparse
import csv
from tkinter import Tk, Label
from time import sleep


def create_csv_file(sbis_exe, prg_file):
    command = r'''{sbis_exe} "/fx:ЗагрузитьФункции(""{prg_file}""); КолвоЗаданий();" '''.format(sbis_exe=sbis_exe,
                                                                                                prg_file=prg_file)
    subprocess.Popen(command)


def show(parse_csv_timeout):
    root_widg = Tk()
    root_widg.title('ДОСКА ПОЗОРА')
    root_widg.geometry("{}x{}+0+0".format(root_widg.winfo_screenwidth(), # Устанавливаем размеры главного окна по размерам монитора.
                                          root_widg.winfo_screenheight()))
    root_widg.attributes('-fullscreen', 1)  # Разворачиваем окно на весь экран.

    label = Label(root_widg, justify='left', wraplength=root_widg.winfo_screenwidth() - 20)
    label.pack(expand=True, fill='both')

    def parse_csv():
        file = open('D:\list.csv')
        reader = csv.reader(file)
        person_tasks = [row for row in reader]
        file.close()
        person_tasks.sort(key=lambda elem: int(elem[1]), reverse=True)  # Сортировка по убыванию кол-ва заданий
        template = 'ДОСКА ПОЗОРА\n\n'
        count = 1
        for person, tasks in person_tasks[:5]:
            template += '{}. {} - {}\n'.format(count, person, tasks)
            count += 1

        label.config(text=template, bg='#FFF6FD', fg='#000000', font=('Segoi UI', 36, 'bold'))  # КРАСНЫЙ
        root_widg.after(parse_csv_timeout, parse_csv)

    # Функция закрывает главное окно по событию.
    def escape(event):
        root_widg.quit()

    # Обработчик потери фокуса окном.
    def leave(event):
        root_widg.attributes('-fullscreen', 1)

    # Обработчик получения фокуса окном.
    def enter(event):
        root_widg.attributes('-fullscreen', 1)

    root_widg.bind('<Escape>', escape)
    root_widg.bind('<Alt-F4>', escape)
    root_widg.bind('<FocusIn>', enter)
    root_widg.bind('<FocusOut>', leave)

    parse_csv()
    root_widg.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sbis_exe', dest='sbis_exe')
    parser.add_argument('-cf', '--csv_file', dest='csv_file')
    parser.add_argument('-prg', '--prg_file', dest='prg_file')
    parser.add_argument('-stm', '--sbis_exe_timeout', dest='sbis_exe_timeout', type=int)
    parser.add_argument('-ptm', '--parse_csv_timeout', dest='parse_csv_timeout', type=int)
    #result = parser.parse_args()
    result = parser.parse_args(['-s', "C:\\Users\\dv.krasnov\\СБиС2\\sbis.exe", '-prg', r"D:\\download\\Список из сбис\\Кол_воЗаданий.prg", '-ptm', '10'])

    #create_csv_file(result.sbis_exe, result.prg_file)
    #sleep(240)
    #print('finish')
    show(result.parse_csv_timeout)
    #while True:
    #    create_csv_file(result.sbis_exe, result.prg_file)
    #    sleep(240)
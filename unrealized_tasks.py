import argparse
import csv
from tkinter import Tk, Label


def show_parsed_csv(parse_csv_timeout):
    root_widg = Tk()
    root_widg.title('НЕЗАКРЫТЫЕ ЗАДАНИЯ')
    root_widg.geometry("{}x{}+0+0".format(root_widg.winfo_screenwidth(), # Устанавливаем размеры главного окна по размерам монитора.
                                          root_widg.winfo_screenheight()))
    root_widg.attributes('-fullscreen', 1)  # Разворачиваем окно на весь экран.

    label = Label(root_widg, justify='left', wraplength=root_widg.winfo_screenwidth() - 20)
    label.pack(expand=True, fill='both')

    def parse_csv():
        file = open(result.csv_file)
        reader = csv.reader(file)
        person_tasks = [row for row in reader]
        file.close()
        person_tasks.sort(key=lambda elem: int(elem[1]), reverse=True)  # Сортировка по убыванию кол-ва заданий
        template = 'НЕЗАКРЫТЫЕ ЗАДАНИЯ\n\n'
        max_len = max([len(elem[0]) for elem in person_tasks[:5]])
        for n, (person, tasks) in enumerate(person_tasks[:5]):
            template += '{}. {:<{max_len}} - {}\n'.format(n+1, person, tasks, max_len=max_len)

        label.config(text=template, bg='#2E00B8', fg='#F5F500', font=('Segoi UI', 36, 'bold'))
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
    parser.add_argument('-cf', '--csv_file', dest='csv_file')
    parser.add_argument('-ptm', '--parse_csv_timeout', dest='parse_csv_timeout', type=int)
    result = parser.parse_args()
    #result = parser.parse_args(['-cf', 'D:\list.csv', '-ptm', '240'])

    show_parsed_csv(result.parse_csv_timeout)

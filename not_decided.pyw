import rpc
from tkinter import Tk
from tkinter import Label


ANS_COUNT = 7  # Количество выводимых заголовков неотвеченных вопросов.
FONT_SIZE = 30  # Размер шрифта.
TIMEOUT = 10000  # Время в милисекундах, по истечении которго будет посылаться запрос на получение данных.


def main():
    # Создание графических элементов. Конифгурирование label будет меняться в зависимости от найденных вопросов.
    root_widg = Tk()
    root_widg.title('Уведомление по неотвеченным вопросам')
    root_widg.geometry("{}x{}+0+0".format(root_widg.winfo_screenwidth(), # Устанавливаем размеры главного окна по размерам монитора.
                                          root_widg.winfo_screenheight()))
    root_widg.attributes('-fullscreen', 1) # Разворачиваем окно на весь экран.

    label = Label(root_widg, justify='left', wraplength=root_widg.winfo_screenwidth() - 20)
    label.pack(expand=True, fill='both')

    def output():
        # Получаем JSON для проверки на наличие вопросов без ответов.
        client = rpc.Client('wi.sbis.ru')
        response = client.call('Вопрос.СписокВопросов', ДопПоля=[], Навигация=None, Сортировка=None, Фильтр=None)

        # Поиск индексов строк с количеством ответов и заголовком.
        title_ind = None
        decided_ind = None
        for i, string in enumerate(response.get('s', [])):
            if string['n'] == 'Title':
                title_ind = i
            if string['n'] == 'Вопрос решен':
                decided_ind = i

        # Конфигурируем label.
        template = ''
        if title_ind and decided_ind:  # если найдены 'Title', 'Вопрос решен'
            count = 0
            for answer in response.get('d', []):
                if not answer[decided_ind]:  # если "Вопрос решен" со значением null
                    count += 1
                    if count <= ANS_COUNT:
                        template += '{}. {}\n'.format(count, answer[title_ind])
            template += '\n\nВсего нерешенных вопросов: {}'.format(count)
            label.config(text=template, bg='#E12019', fg='#FFFFFF', font=('Segoi UI', FONT_SIZE, 'bold'))  # КРАСНЫЙ
            if count == 0:
                template = 'Все вопросы решены'
                label.config(text=template, bg='#27AE60', fg='#FFFFFF', font=('Segoi UI', FONT_SIZE, 'bold'))  # ЗЕЛЁНЫЙ
        else:
            template = 'Сценарий не нашел индекс для "Title", "Вопрос решен" в ответе на запрос'
            label.config(text=template, bg='#78207E', fg='#4FEDEE', font=('Segoi UI', FONT_SIZE, 'bold'))  # ФИОЛЕТОВЫЙ

        # Для циклической отправки запроса client.call() по истичении TIMEOUT
        root_widg.after(TIMEOUT, output)

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

    output() # Вызывается один раз, чтобы послать первый запрос, не дожидаясь потока из метода root_widg.after()
    root_widg.mainloop()


if __name__ == '__main__':
    main()
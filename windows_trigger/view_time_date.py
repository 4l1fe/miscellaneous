from tkinter import Tk, Label
from datetime import datetime

root = Tk()
root.title('Clock')
x, y = root.maxsize()
root.overrideredirect(True)

label_time = Label(root)
label_time.pack(expand=True, fill='both')
label_date = Label(root)
label_date.pack(expand=True, fill='both')


def change_time_date():
    now = datetime.now().strftime('%H:%M:%S')
    today = datetime.today().strftime('%d.%m.%y')
    time_text = '{}'.format(now)
    date_text = '{}'.format(today)
    label_time.config(text=time_text, bg='#000000', fg='#FFFFFF', font=('Segoi UI', 60, 'bold'))
    label_date.config(text=date_text, bg='#000000', fg='#FFFFFF', font=('Segoi UI', 30, 'bold'))
    root.geometry('+{x}+{y}'.format(x=x-label_time.winfo_width(),
                                    y=y-label_time.winfo_height()-label_date.winfo_height()))
    root.after(1000, change_time_date)

change_time_date()
root.mainloop()

import tkinter as tk
from tkinter import ttk
import re


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Validation Demo')

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # label
        ttk.Label(text='Email:').grid(row=0, column=0, padx=5, pady=5)

        # email entry
        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid),)

        self.email_entry = ttk.Entry(self, width=50)
        self.email_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.email_entry.grid(row=0, column=1, columnspan=2, padx=5)

        self.label_error = ttk.Label(self, foreground='red')
        self.label_error.grid(row=1, column=1, sticky=tk.W, padx=5)

        # button
        self.send_button = ttk.Button(text='Send').grid(row=0, column=4, padx=5)

    def show_message(self, error='', color='black'):
        self.label_error['text'] = error
        self.email_entry['foreground'] = color

    def validate(self, value):
        """
        Validat the email entry
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value) is None:
            return False

        self.show_message()
        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        self.show_message('Please enter a valid email', 'red')


if __name__ == '__main__':
    app = App()
    app.mainloop()
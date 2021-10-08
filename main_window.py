#!/usr/bin/env python3
"""Главное окно приложения"""

ERROR_PYTHON_VERSION = 1

import sys

if sys.version_info < (3, 6):
    print('Use python >= 3.6', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

__version__ = '1.1'
__author__ = 'Vikhlyantseva Darya'
__email__ = 'dashav1605@gmail.com'

import tkinter
from tkinter import ttk
from keyboard_tutor import KeyboardTutor


class SpeedLabel:
    def __init__(self, frame):
        self.counter = tkinter.StringVar()
        self.counter.set(0)
        speed_text = tkinter.Label(frame, text="Current speed (sym / min): ",
                                   font=('Arial', 12, 'bold'))
        speed_counter = tkinter.Label(frame, textvariable=self.counter,
                                      font=('Arial', 12), anchor="e", width=5)
        speed_counter.pack(side=tkinter.RIGHT, padx=10)
        speed_text.pack(side=tkinter.RIGHT)


class SymbolsCounterLabel:
    def __init__(self, frame):
        self.counter = tkinter.StringVar()
        self.counter.set(0)
        symbols_count_text = tkinter.Label(frame, text="Symbols:",
                                           font=('Arial', 12, 'bold'))
        symbols_count_text.pack(side=tkinter.LEFT, padx=10)
        symbols_count = tkinter.Label(frame, textvariable=self.counter,
                                      font=('Arial', 12), anchor="w")
        symbols_count.pack(side=tkinter.LEFT, padx=5)


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard Tutor")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.minsize(600, 300)
        self.geometry(f"+{self.winfo_screenwidth() // 5}"
                      f"+{self.winfo_screenheight() // 5}")
        self.resizable(width=False, height=False)
        self.font = ('Arial', 12)
        self.option_add('*TCombobox*Listbox.font', self.font)

        bottom_frame = tkinter.Frame(self)
        bottom_frame.pack(side=tkinter.BOTTOM, fill='x')

        top_frame = tkinter.Frame(self)
        top_frame.pack(side=tkinter.TOP, fill='x')

        center_frame = tkinter.Frame(self)
        center_frame.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        symbols_counter_label = SymbolsCounterLabel(top_frame)
        speed_label = SpeedLabel(top_frame)

        topic = ttk.Combobox(top_frame, values=['Letters', 'Punctuation',
                                                'Numbers', 'Words',
                                                'Quotations', 'Long Text',
                                                'Python', 'TypeScript'],
                             font=self.font, state='readonly')
        topic.set('Choose training topic')
        topic.pack(side=tkinter.TOP)

        keyboard_tutor = KeyboardTutor(center_frame,
                                       symbols_counter_label.counter,
                                       speed_label.counter, topic, top_frame)

        quit_button = tkinter.Button(bottom_frame, text='Quit',
                                     font=('Arial', 12), command=self.quit)
        quit_button.pack(side=tkinter.RIGHT, padx=10, pady=5)

        reload_button = tkinter.Button(bottom_frame, text='Reload text',
                                       font=('Arial', 12),
                                       command=keyboard_tutor.reload_text_button)
        reload_button.pack(side=tkinter.LEFT, padx=10, pady=5)


main = MainWindow()
main.mainloop()

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
from keyboard_tutor import KeyboardTutor


class WordsCounterLabel:
    def __init__(self, frame):
        self.counter = tkinter.StringVar()
        self.counter.set(0)
        words_count_text = tkinter.Label(frame, text="Words:", font=('Arial', 12, 'bold'))
        words_count_text.grid(row=0, padx=5)
        words_count = tkinter.Label(frame, textvariable=self.counter, font=('Arial', 12), anchor="w")
        words_count.grid(row=0, column=1)


class SymbolsCounterLabel:
    def __init__(self, frame):
        self.counter = tkinter.StringVar()
        self.counter.set(0)
        symbols_count_text = tkinter.Label(frame, text="Symbols:", font=('Arial', 12, 'bold'))
        symbols_count_text.grid(row=0, column=2)
        symbols_count = tkinter.Label(frame, textvariable=self.counter, font=('Arial', 12), anchor="w")
        symbols_count.grid(row=0, column=3)


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keyboard Tutor")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.geometry(f"+{self.winfo_screenwidth() // 5}+{self.winfo_screenheight() // 5}")
        self.resizable(width=False, height=False)

        bottom_frame = tkinter.Frame(self)
        bottom_frame.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.BOTH)

        top_frame = tkinter.Frame(self)
        top_frame.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        center_frame = tkinter.Frame(self)
        center_frame.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        words_counter_label = WordsCounterLabel(top_frame)
        symbols_counter_label = SymbolsCounterLabel(top_frame)
        keyboard_tutor = KeyboardTutor(center_frame, words_counter_label.counter, symbols_counter_label.counter)

        quit_button = tkinter.Button(bottom_frame, text='Quit', font=('Arial', 12), command=self.quit)
        quit_button.pack(side=tkinter.RIGHT, padx=5, pady=5)

        reload_button = tkinter.Button(bottom_frame, text='Reload Text', font=('Arial', 12),
                                       command=keyboard_tutor.reload_text)
        reload_button.pack(side=tkinter.LEFT, padx=5, pady=5)


main = MainWindow()
main.mainloop()

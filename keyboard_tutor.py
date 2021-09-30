#!/usr/bin/env python3
"""Логика клавиатурного тренажера"""

import tkinter
import time
import json
import random
from text_cleaner import TextCleaner

VALID_SYMBOLS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
                 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'y',
                 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R',
                 'T', 'Z', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
                 'G', 'H', 'J', 'K', 'L', 'Y', 'X', 'C', 'V', 'B',
                 'N', 'M', '^', '!', '"', '$', '%', '&', "/", '(',
                 ')', '=', '?', ' ', '+', '<', ',', '.', '-', '_',
                 '*', '#', "'", ':', ';', '>', '@', '{', '[', ']', '}']


class KeyboardTutor(tkinter.Text):
    def __init__(self, frame, words_counter, symbols_counter):

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        super().__init__(frame, wrap=tkinter.WORD, bg="white", height=20, width=75, font=('Arial', 15),
                         yscrollcommand=scrollbar.set, padx=5, pady=10, borderwidth=5)
        scrollbar.config(command=self.yview)
        self.pack(expand=True, fill="both")

        self.tag_config("correct", background="white smoke", foreground="green")
        self.tag_config("incorrect", background="misty rose", foreground="red")
        self.tag_config("corrected", background="white smoke", foreground="#465945")
        self.tag_config("current_position", background="#FFDB58", foreground="black")

        self.bind_all('<Key>', self.type)

        self.steps = ["Let's typing", "Training", "Results"]
        self.current_step = 0
        self.start_time = 0
        self.finish_time = 0

        self.text = ''
        self.chars_count = 0
        self.words_counter = words_counter
        self.symbols_counter = symbols_counter
        self.mistakes_count = 0

        self.texts = []
        self.load_texts()
        self.show()

    def do_first_step(self):
        self.insert(tkinter.END, "Let's typing!\n\nPress any key to start.\n")
        self.chars_count = 0
        self.words_counter.set(0)
        self.symbols_counter.set(0)
        self.mistakes_count = 0
        self.text = random.choice(self.texts)

    def do_training_step(self):
        self.chars_count = len(self.text)
        self.symbols_counter.set(self.chars_count)
        self.words_counter.set(len(self.text.split()))
        self.insert(tkinter.END, self.text)
        self.insert(tkinter.END, '\u23CE\n')
        self.mark_set("current_position_mark", "0.0")
        self.mark_set("correct_mark", "0.0")
        self.tag_add("current_position", "current_position_mark")
        self.incorrect = set()
        self.corrected = set()
        self.start_time = time.time()

    def get_results(self):
        self.finish_time = time.time() - self.start_time
        minutes = int(self.finish_time / 60)
        sec = self.finish_time % 60
        cps = self.chars_count / self.finish_time
        wpm = cps * 60 / 5
        acc = 100 * (1 - self.mistakes_count / self.chars_count)
        return ["Your results is here!\n\n",
                f"Average time: {minutes} min {round(sec)} sec.\n",
                f"Characters per second: {round(cps, 1)}.\n",
                f"Words per minute: {round(wpm, 1)}.\n",
                f"Mistakes: {self.mistakes_count}.\n",
                f"Accuracy: {round(acc, 1)}%.\n",
                f"\nPress any key to start next training.\n\n"]

    def show(self):
        self.config(state=tkinter.NORMAL)
        self.delete("0.0", tkinter.END)

        step = self.steps[self.current_step]
        if step == "Let's typing":
            self.do_first_step()
        elif step == "Training":
            self.do_training_step()
        elif step == "Results":
            for line in self.get_results():
                self.insert(tkinter.END, line)

        self.config(state=tkinter.DISABLED)

    def load_texts(self):
        with open("texts.json") as file:
            texts_json = json.load(file)
            self.texts = [TextCleaner(txt).text for txt in texts_json.values()]

    @staticmethod
    def check_and_get_char(event):
        key = event.char
        if key in VALID_SYMBOLS:
            return key
        key = event.keysym
        if key == 'BackSpace' or key == "Return":
            return key
        return

    def change_step(self):
        self.current_step += 1
        if self.current_step == 3:
            self.current_step = 0
        self.show()

    def reload_text(self):
        self.current_step = 0
        self.show()

    def is_corrected_mistake(self, move_correct, key):
        return move_correct and key != 'BackSpace' and self.index('current_position_mark') in self.incorrect

    def is_made_mistake(self, move_correct, key):
        return not move_correct or self.compare('current_position_mark', '!=', 'correct_mark') and key != 'BackSpace'

    def type(self, event):
        if self.steps[self.current_step] == 'Training':
            key = self.check_and_get_char(event)
            current_char = self.get(self.tag_ranges('current_position')[0],
                                    self.tag_ranges('current_position')[1])
            if key:
                move_correct = (key == current_char or (key == "Return" and current_char == '\u23CE')
                                or key == "BackSpace")

                if self.is_corrected_mistake(move_correct, key):
                    self.incorrect.remove(self.index('current_position_mark'))
                    self.corrected.add(self.index('current_position_mark'))

                if self.is_made_mistake(move_correct, key):
                    self.mistakes_count += 1
                    self.incorrect.add(self.index('current_position_mark'))

                self.remove_tags()
                self.update_marks(move_forward=(key != 'BackSpace'), move_correct=move_correct)
                self.add_tags()

            if self.is_end_of_text():
                self.change_step()
        else:
            self.change_step()

    def update_marks(self, move_forward=True, move_correct=True):
        if move_correct and self.compare('current_position_mark', '==', 'correct_mark'):
            self.move_mark('correct_mark', move_forward)
        self.move_mark('current_position_mark', move_forward)

    def is_end_of_line(self, line, char):
        return self.index(f"{line}.end") == f"{line}.{char + 1}"

    @staticmethod
    def is_first_symbol_in_line(line, char):
        return char == 0 and line > 1

    def move_mark(self, mark_name, move_forward):
        line, char = map(int, str.split(self.index(mark_name), "."))
        if move_forward:
            step = 1
            if self.is_end_of_line(line, char):
                line += 1
                char = -1
        else:
            step = -1
            if self.is_first_symbol_in_line(line, char):
                line, char = map(int, self.index(f"{line - 1}.end").split("."))
        self.mark_set(mark_name, f"{line}.{char + step}")

    def remove_tags(self):
        self.tag_remove("correct", "0.0", "correct_mark")
        self.tag_remove("current_position", "current_position_mark")
        [self.tag_remove('incorrect', inc) for inc in self.incorrect]
        [self.tag_remove('corrected', c) for c in self.corrected]

    def add_tags(self):
        self.tag_add("correct", "0.0", 'correct_mark')
        self.tag_add("current_position", "current_position_mark")
        [self.tag_add('incorrect', inc) for inc in self.incorrect]
        [self.tag_add('corrected', c) for c in self.corrected]

    def is_end_of_text(self):
        line, column = map(int, self.index('correct_mark').split("."))
        end_line, end_column = map(int, self.index(tkinter.END).split("."))
        return line + 1 == end_line and column == end_column

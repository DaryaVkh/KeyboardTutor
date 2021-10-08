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
                 '*', '#', "'", ':', ';', '>', '@', '{', '[', ']',
                 '}']

FIRST_MESSAGE = "Let's typing! " \
                "Choose training topic at the top of the window.\n\n" \
                "If you are new, you can warm up with easy and fast topic " \
                "\"Letters\", \"Numbers\" or \"Punctuation\".\n\n" \
                "If you want something more serious and hard, you can choose " \
                "\"Words\", \"Quotations\" or \"Long Text\".\n\n" \
                "If you want something special, you can choose \"Python\" or \"TypeScript\" " \
                "to practice fast typing some of key words of this programming languages."


class KeyboardTutor(tkinter.Text):
    def __init__(self, frame, symbols_counter, current_speed_counter, text_topic, frame_for_focus):

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        super().__init__(frame, wrap=tkinter.WORD, bg="white", height=20,
                         width=75, font=('Times', 17), yscrollcommand=scrollbar.set,
                         padx=5, pady=10, borderwidth=5)
        scrollbar.config(command=self.yview)
        self.pack(expand=True, fill="both")

        self.tag_config("correct", background="white smoke", foreground="#465945")
        self.tag_config("incorrect", background="misty rose", foreground="red")
        self.tag_config("current_position", background="#FFDB58")

        self.bind_all('<Key>', self.type)

        self.steps = ["Start", "Training", "Results"]
        self.current_step = 0
        self.start_time = 0
        self.end_time = 0

        self.text = ''
        self.symbols_count = 0
        self.printed_symbols_count = 0
        self.symbols_counter = symbols_counter
        self.current_speed_counter = current_speed_counter
        self.mistakes_count = 0
        self.frame_for_focus = frame_for_focus

        self.texts_json = None
        self._load_texts()
        self.text_topic = text_topic
        self.text_topic.bind("<<ComboboxSelected>>", self.reload_text)
        self.show()

    def _load_quotations(self):
        self.text = TextCleaner.clean_text(
            random.choice(self.texts_json["Quotations"]))

    def _load_long_text(self):
        self.text = random.choice(self.texts_json["Long Text"])

    def _load_numbers(self):
        numbers_count = random.randint(50, 71)
        text = f'{random.randint(0, 1000)}'
        for _ in range(numbers_count):
            text += f' {random.randint(0, 1000000)}'
        self.text = text

    def _load_symbols(self, topic):
        count = random.randint(50, 71)
        text = f'{random.choice(self.texts_json[topic])}'
        for _ in range(count):
            text += f' {random.choice(self.texts_json[topic])}'
        self.text = text

    def _load_words(self):
        words_count = random.randint(20, 41)
        text = f'{random.choice(self.texts_json["Words"])}'
        for _ in range(words_count):
            if random.choice([True, False]):
                text += f'\n{random.choice(self.texts_json["Words"])}'
            else:
                text += f'\n{random.choice(self.texts_json["Words"]).title()}'
        self.text = text

    def _load_programming_languages(self, topic):
        words_count = random.randint(20, 41)
        text = f'{random.choice(self.texts_json[topic])}'
        for _ in range(words_count):
            text += f'\n{random.choice(self.texts_json[topic])}'
        self.text = text

    def _load_text(self):
        topic = self.text_topic.get()
        if topic == "Quotations":
            self._load_quotations()
        elif topic == "Long Text":
            self._load_long_text()
        elif topic == "Numbers":
            self._load_numbers()
        elif topic == "Letters" or topic == "Punctuation":
            self._load_symbols(topic)
        elif topic == "Words":
            self._load_words()
        else:
            self._load_programming_languages(topic)

    def do_first_step(self):
        if self.text_topic.get() == "Choose training topic":
            self.insert(tkinter.END, FIRST_MESSAGE)
        else:
            self.insert(tkinter.END, "Text loaded!\n\nPress any key to start.\n")
        self.symbols_count = 0
        self.symbols_counter.set(0)
        self.current_speed_counter.set(0)
        self.mistakes_count = 0

    def do_training_step(self):
        self._load_text()
        self.symbols_count = len(self.text)
        self.symbols_counter.set(self.symbols_count)
        self.printed_symbols_count = 0
        self.insert(tkinter.END, self.text)
        self.insert(tkinter.END, '\u23CE\n')
        self.mark_set("current_position_mark", "0.0")
        self.mark_set("correct_mark", "0.0")
        self.tag_add("current_position", "current_position_mark")
        self.incorrect = None
        self.start_time = time.time()

    def get_results(self):
        self.end_time = time.time() - self.start_time
        min = self.end_time / 60
        sec = self.end_time % 60
        cps = self.symbols_count / self.end_time
        wpm = cps * 60 / 5
        accuracy = 100 * (1 - self.mistakes_count / self.symbols_count)
        return ["Your results is here!\n\n",
                f"Average time: {int(min)} min {round(sec)} sec.\n",
                f"Characters per second: {round(cps, 1)}.\n",
                f"Words per minute: {round(wpm, 1)}.\n",
                f"Mistakes: {self.mistakes_count}.\n",
                f"Accuracy: {round(accuracy, 1)}%.\n",
                f"\nPress any key to start next training.\n\n"]

    def show(self):
        self.config(state=tkinter.NORMAL)
        self.delete("0.0", tkinter.END)

        step = self.steps[self.current_step]
        if step == "Start":
            self.do_first_step()
        elif step == "Training":
            self.do_training_step()
        elif step == "Results":
            for line in self.get_results():
                self.insert(tkinter.END, line)

        self.config(state=tkinter.DISABLED)

    def _load_texts(self):
        with open("texts.json") as file:
            self.texts_json = json.load(file)

    @staticmethod
    def check_and_get_char(event):
        key = event.char
        if key in VALID_SYMBOLS:
            return key
        key = event.keysym
        if key == 'Return':
            return key
        return

    def change_step(self):
        self.current_step += 1
        if self.current_step == 3:
            self.current_step = 0
        self.show()

    def reload_text_with_button(self):
        self.current_step = 0
        self.show()

    def reload_text(self, event):
        self.current_step = 0
        self.frame_for_focus.focus()
        self.show()

    def is_made_mistake(self, move_correct):
        return not move_correct \
               or self.compare('current_position_mark', '!=', 'correct_mark')

    def type(self, event):
        if self.steps[self.current_step] == 'Training':
            self.current_speed_counter.set(round(self.printed_symbols_count /
                                                 (time.time() - self.start_time) * 60, 2))
            key = self.check_and_get_char(event)
            current_char = self.get(self.tag_ranges('current_position')[0],
                                    self.tag_ranges('current_position')[1])
            if key:
                move_correct = (key == current_char or (key == "Return"
                                                        and current_char == '\u23CE'))
                if move_correct:
                    self.printed_symbols_count += 1

                if self.is_made_mistake(move_correct):
                    self.mistakes_count += 1

                self.remove_tags()
                self.update_marks(move_correct)
                self.add_tags()

                self.scroll()

            if self.is_end_of_text():
                self.change_step()
        elif self.text_topic.get() != "Choose training topic":
            self.change_step()

    def scroll(self):
        current_y = self.dlineinfo('current_position_mark')[1]
        height = self.winfo_height()
        if current_y + 80 > height:
            self.yview_scroll(height // 2, 'pages')

    def update_marks(self, move_correct=True):
        if move_correct:
            if self.incorrect:
                self.incorrect = None
                self.tag_remove('incorrect', 'current_position_mark')
            self.move_mark('correct_mark')
            self.move_mark('current_position_mark')
        elif not self.incorrect:
            self.incorrect = self.index('current_position_mark')
            self.tag_add('incorrect', 'current_position_mark')

    def is_end_of_line(self, line, char):
        return self.index(f"{line}.end") == f"{line}.{char + 1}"

    @staticmethod
    def is_first_symbol_in_line(line, char):
        return char == 0 and line > 1

    def move_mark(self, mark_name):
        line, char = map(int, str.split(self.index(mark_name), "."))
        step = 1
        if self.is_end_of_line(line, char):
            line += 1
            char = -1
        self.mark_set(mark_name, f"{line}.{char + step}")

    def remove_tags(self):
        self.tag_remove("correct", "0.0", "correct_mark")
        self.tag_remove("current_position", "current_position_mark")

    def add_tags(self):
        self.tag_add("correct", "0.0", 'correct_mark')
        self.tag_add("current_position", "current_position_mark")

    def is_end_of_text(self):
        line, column = map(int, self.index('correct_mark').split("."))
        end_line, end_column = map(int, self.index(tkinter.END).split("."))
        return line + 1 == end_line and column == end_column

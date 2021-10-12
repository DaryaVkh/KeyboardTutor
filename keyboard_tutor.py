#!/usr/bin/env python3
"""Логика клавиатурного тренажера"""

import tkinter
import time
import json
import random
import pygame
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
                "If you want something more serious and hard, you can " \
                "choose \"Words\", \"Quotations\" or \"Long Text\".\n\n" \
                "If you want something special, you can choose \"Python\" " \
                "or \"TypeScript\" to practice fast typing some of key " \
                "words of this programming languages."


class Table:
    def __init__(self, root, rows, columns, values):
        for i in range(rows):
            for j in range(columns):
                self.e = tkinter.Entry(root, width=16, font=('Arial', 12),
                                       justify=tkinter.CENTER)
                if i == 0:
                    self.e.config(font=('Arial', 13, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(tkinter.END, values[i][j])
                self.e.config(state="readonly")


class ProgressTableWindow(tkinter.Toplevel):
    def __init__(self, main):
        super().__init__(master=main)
        self.title("Progress")
        self.resizable(width=False, height=False)

        columns = ['Training topic', 'Best time', 'Best speed (s/m)',
                   'Last time', 'Last speed (s/m)']
        with open("progress.json") as file:
            self.progress_json = json.load(file)

        lttrs = self.progress_json["Letters"]
        pct = self.progress_json["Punctuation"]
        nmbrs = self.progress_json["Numbers"]
        words = self.progress_json["Words"]
        qts = self.progress_json["Quotations"]
        long = self.progress_json["Long Text"]
        py = self.progress_json["Python"]
        tps = self.progress_json["TypeScript"]
        values = [columns,
                  ['Letters', f'{lttrs["Best time"]}', f'{lttrs["Best speed"]}'
                      , f'{lttrs["Last time"]}', f'{lttrs["Last speed"]}'],
                  ['Punctuation', f'{pct["Best time"]}', f'{pct["Best speed"]}'
                      , f'{pct["Last time"]}', f'{pct["Last speed"]}'],
                  ['Numbers', f'{nmbrs["Best time"]}', f'{nmbrs["Best speed"]}'
                      , f'{nmbrs["Last time"]}', f'{nmbrs["Last speed"]}'],
                  ['Words', f'{words["Best time"]}', f'{words["Best speed"]}',
                   f'{words["Last time"]}', f'{words["Last speed"]}'],
                  ['Quotations', f'{qts["Best time"]}', f'{qts["Best speed"]}',
                   f'{qts["Last time"]}', f'{qts["Last speed"]}'],
                  ['Long Text', f'{long["Best time"]}', f'{long["Best speed"]}'
                      , f'{long["Last time"]}', f'{long["Last speed"]}'],
                  ['Python', f'{py["Best time"]}', f'{py["Best speed"]}'
                      , f'{py["Last time"]}', f'{py["Last speed"]}'],
                  ['TypeScript', f'{tps["Best time"]}', f'{tps["Best speed"]}',
                   f'{tps["Last time"]}', f'{tps["Last speed"]}']]
        self.table = Table(self, 9, 5, values)


class KeyboardTutor(tkinter.Text):
    def __init__(self, frame, current_speed_counter,
                 text_topic, frame_for_focus):

        scrollbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        super().__init__(frame, wrap=tkinter.WORD, bg="white", height=20,
                         width=75, font=('Times', 17),
                         yscrollcommand=scrollbar.set,
                         padx=5, pady=10, borderwidth=5)
        scrollbar.config(command=self.yview)
        self.pack(expand=True, fill="both")

        self.tag_config("correct", background="white smoke",
                        foreground="#465945")
        self.tag_config("incorrect", background="misty rose",
                        foreground="red")
        self.tag_config("current_position", background="#FFDB58")

        self.bind_all('<Key>', self.type)

        self.steps = ["Start", "Training", "Results"]
        self.current_step = 0
        self.start_time = 0
        self.end_time = 0

        self.text = ''
        self.symbols_count = 0
        self.printed_symbols_count = 0
        self.current_speed_counter = current_speed_counter
        self.mistakes_count = 0
        self.frame_for_focus = frame_for_focus

        self.is_sound_off = False
        pygame.mixer.init(44100, -16, 2, 2048)
        self.wa_sound = pygame.mixer.Sound('WA.wav')

        self.texts_json = None
        self._load_texts()
        self.text_topic = text_topic
        self.text_topic.bind("<<ComboboxSelected>>",
                             self.reload_text_with_change_topic)
        self.show()

    def sound_off(self):
        self.is_sound_off = True

    def sound_on(self):
        self.is_sound_off = False

    def _load_quotations(self):
        self.text = TextCleaner.clean_text(
            random.choice(self.texts_json["Quotations"]))

    def _load_long_text(self):
        self.text = random.choice(self.texts_json["Long Text"])

    def _load_numbers(self):
        numbers_count = random.randint(30, 51)
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
            self.insert(tkinter.END, "Text loaded!"
                                     "\n\nPress any key to start.\n")
        self.current_speed_counter.set(0)
        self.mistakes_count = 0

    def do_training_step(self):
        self._load_text()
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
        symbols_count = len(self.text)
        min = int(self.end_time / 60)
        sec = round(self.end_time % 60)
        sps = round(symbols_count / self.end_time, 1)
        spm = round(self.printed_symbols_count /
                    (time.time() - self.start_time) * 60, 2)
        wpm = round(sps * 60 / 5, 1)
        accuracy = round(100 * (1 - self.mistakes_count / symbols_count), 1)

        self._update_progress(min, sec, spm)

        return ["Your results is here!\n\n",
                f"Average time: {min} min {sec} sec.\n",
                f"Symbols count: {symbols_count}.\n",
                f"Symbols per second: {sps}.\n",
                f"Symbols per minute: {spm}.\n"
                f"Words per minute: {wpm}.\n",
                f"Mistakes: {self.mistakes_count}.\n",
                f"Accuracy: {accuracy}%.\n",
                f"\nPress any key to start next training.\n\n"]

    def _update_progress(self, min, sec, spm):
        with open('progress.json') as file:
            progress_json = json.load(file)

        current_time = f"{min} min {sec} sec"
        text_topic = self.text_topic.get()
        progress_record = progress_json[text_topic]

        progress_record["Last time"] = current_time
        progress_record["Last speed"] = spm

        prev_best_time = progress_record["Best time"]
        if prev_best_time != 0:
            prev_best_time = prev_best_time.split(' ')
            if int(prev_best_time[0]) > min \
                    or int(prev_best_time[0]) == min \
                    and int(prev_best_time[2]) > sec:
                progress_record["Best time"] = current_time
            if spm > float(progress_json[text_topic]["Best speed"]):
                progress_record["Best speed"] = spm
        else:
            progress_record["Best time"] = current_time
            progress_record["Best speed"] = spm

        with open('progress.json', "w", encoding='utf-8') as f:
            json.dump(progress_json, f)

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

    def reload_text(self):
        self.current_step = 0
        self.show()

    def reload_text_with_change_topic(self, event):
        self.current_step = 0
        self.frame_for_focus.focus()
        self.show()

    def is_made_mistake(self, move_correct):
        return not move_correct \
               or self.compare('current_position_mark', '!=', 'correct_mark')

    def type(self, event):
        if self.steps[self.current_step] == 'Training':
            self.current_speed_counter.set(
                round(self.printed_symbols_count /
                      (time.time() - self.start_time) * 60, 2))
            key = self.check_and_get_char(event)
            current_char = self.get(self.tag_ranges('current_position')[0],
                                    self.tag_ranges('current_position')[1])
            if key:
                move_correct = (key == current_char or
                                (key == "Return" and current_char == '\u23CE'))
                if move_correct:
                    if not self.is_sound_off:
                        self.wa_sound.stop()
                    self.printed_symbols_count += 1

                if self.is_made_mistake(move_correct):
                    if not self.is_sound_off:
                        self.wa_sound.play()
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

    def load_progress(self):
        ProgressTableWindow(self)

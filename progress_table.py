#!/usr/bin/env python3
"""Окно с таблицей прогресса"""

import tkinter
import json


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

        ltrs = self.progress_json["Letters"]
        pt = self.progress_json["Punctuation"]
        nmrs = self.progress_json["Numbers"]
        words = self.progress_json["Words"]
        qts = self.progress_json["Quotations"]
        lng = self.progress_json["Long Text"]
        py = self.progress_json["Python"]
        tps = self.progress_json["TypeScript"]
        values = [columns,
                  ['Letters', f'{ltrs["Best time"]}', f'{ltrs["Best speed"]}',
                   f'{ltrs["Last time"]}', f'{ltrs["Last speed"]}'],
                  ['Punctuation', f'{pt["Best time"]}', f'{pt["Best speed"]}',
                   f'{pt["Last time"]}', f'{pt["Last speed"]}'],
                  ['Numbers', f'{nmrs["Best time"]}', f'{nmrs["Best speed"]}',
                   f'{nmrs["Last time"]}', f'{nmrs["Last speed"]}'],
                  ['Words', f'{words["Best time"]}', f'{words["Best speed"]}',
                   f'{words["Last time"]}', f'{words["Last speed"]}'],
                  ['Quotations', f'{qts["Best time"]}', f'{qts["Best speed"]}',
                   f'{qts["Last time"]}', f'{qts["Last speed"]}'],
                  ['Long Text', f'{lng["Best time"]}', f'{lng["Best speed"]}',
                   f'{lng["Last time"]}', f'{lng["Last speed"]}'],
                  ['Python', f'{py["Best time"]}', f'{py["Best speed"]}',
                   f'{py["Last time"]}', f'{py["Last speed"]}'],
                  ['TypeScript', f'{tps["Best time"]}', f'{tps["Best speed"]}',
                   f'{tps["Last time"]}', f'{tps["Last speed"]}']]
        self.table = Table(self, 9, 5, values)

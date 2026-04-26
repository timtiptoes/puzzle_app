import os
import csv
import datetime
import re
import random
import numpy as np
from .lib import *
from .lib import docparts


class document(object):
    def __init__(self, fname, title="", savetex=True):
        self.savetex = savetex
        self.main = []
        self.fname = fname

    def add(self, code):
        self.main.append(code)

    def write_compile(self, remove_aux=True):
        with open("tmp/%s.tex" % self.fname, "wb") as f:
            f.write('\n'.join(self.main).encode('utf-8'))
        os.system("pdflatex --output-directory tmp tmp/%s.tex" % self.fname)
        now = datetime.datetime.now().isoformat()
        os.system("cp tmp/{}.pdf log/{}_{}.pdf".format(self.fname, self.fname, now))
        os.remove("tmp/%s.log" % self.fname)
        if remove_aux:
            os.remove("tmp/%s.aux" % self.fname)
        if not self.savetex:
            os.remove("tmp/%s.tex" % self.fname)


class crossword1d(object):

    def __init__(self, fname, title="", clue="gimme", savetex=False):
        with open('static/' + fname + ".csv", mode='r') as csvfile:
            reader = csv.reader(csvfile, quotechar='"')
            self.s = {rows[0]: rows[1] for rows in reader}

        self.fname = fname.replace(" ", "").lower().replace(".csv", "")
        self.clue = clue.upper()
        self.crossword_puzzle = document(self.fname)
        self.title = title
        self.puzzle_lines = []
        self.hint_lines = []
        self.puzzle_list = list()
        self.pos = {}
        self.hints = []
        self.width_of_puzzle = 0

    def add_section(self, *args, **kwargs):
        start, middle, end = docparts.crossword_parts(title=self.title)
        self.choose_words()
        self.make_puzzle_lines()
        self.make_hint_lines()

        self.crossword_puzzle.add(start)
        self.crossword_puzzle.add("\\begin{Puzzle}{" + str(self.width_of_puzzle) + "}{" + str(len(self.puzzle_list)) + "}")
        self.crossword_puzzle.add('\n'.join(self.puzzle_lines))
        self.crossword_puzzle.add(middle)
        self.crossword_puzzle.add('\n'.join(self.hint_lines))
        self.crossword_puzzle.add(end)

    def layout_line(self, line, clue_num, clue_column):
        output_line = "|"
        numbered = False
        for i in range(len(line)):
            ch = line[i]
            if ch == '-':
                col_str = '{}'
            else:
                if not numbered:
                    col_str = "[" + str(clue_num) + "]"
                    numbered = True
                else:
                    col_str = "[]"
                if i == clue_column:
                    col_str += "[O]"
                col_str += ch
            output_line = output_line + col_str + "|"
        return output_line + "."

    def choose_words(self, *args, **kwargs):
        glossary = list(self.s.keys())
        max_to_right = 0
        max_to_left = 0
        for ch in self.clue.replace(" ", ""):
            cnt = 0
            while cnt < 40:
                one_word = random.choice(glossary)
                if ch in one_word.upper() and one_word not in self.puzzle_list:
                    self.puzzle_list.append(one_word)
                    chars_to_left = one_word.upper().index(ch) - 1
                    chars_to_right = len(one_word) - chars_to_left - 1
                    max_to_left = max(chars_to_left, max_to_left)
                    max_to_right = max(chars_to_right, max_to_right)
                    self.pos[one_word] = (chars_to_left, chars_to_right)
                    break
                cnt += 1

        self.width_of_puzzle = max_to_left + max_to_right + 1
        self.max_to_left = max_to_left
        self.max_to_right = max_to_right

    def make_puzzle_lines(self, *args, **kwargs):
        for i in range(len(self.puzzle_list)):
            word = self.puzzle_list[i]
            word_choices = ""
            tex_formatted_line = self.layout_line(
                '-' * (self.max_to_left - self.pos[word][0]) + word.replace(" ", "") + '-' * (self.max_to_right - self.pos[word][1]),
                i + 1,
                self.max_to_left + 1,
            )
            self.puzzle_lines.append(tex_formatted_line)
            if re.search('Vocabulary', self.title):
                available_words = list(filter(lambda x: x != word and len(x) == len(word), self.s.keys()))
                chosen_words = [available_words[j] for j in np.random.choice(len(available_words), size=4, replace=False)]
                chosen_words.append(word)
                random.shuffle(chosen_words)
                word_choices = " One of " + ", ".join(chosen_words[:-1]) + " or " + chosen_words[-1]
            self.hints.append("\\Clue{" + str(i + 1) + "}{" + word.upper() + "}{" + self.s[word] + word_choices + "}")

    def make_hint_lines(self, *args, **kwargs):
        second_half_flag = False
        for i in range(len(self.hints)):
            if i > len(self.puzzle_list) / 2 and not second_half_flag:
                self.hint_lines.append('\\end{PuzzleClues}')
                self.hint_lines.append('\\begin{PuzzleClues}{\\textbf{ }}\\\\')
                second_half_flag = True
            self.hint_lines.append(self.hints[i] + "\\" + "\\" + "\\")

    def write(self):
        self.crossword_puzzle.write_compile()


if __name__ == "__main__":
    mycrossword = crossword1d("BU", clue="jeans", savetex=True)
    mycrossword.add_section()
    mycrossword.write()

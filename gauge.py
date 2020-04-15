#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from curses import wrapper
import curses
import fileinput
import time
import locale
import argparse

locale.setlocale(locale.LC_ALL, '')

parser = argparse.ArgumentParser()
parser.add_argument("-f", action='store_true', help='the -f option causes gauge to keep reading from the input')
parser.add_argument("-i", type=float, default=0.1, help='graphing interval in seconds when using -f (default = 1)')
parser.add_argument("files", metavar="file", nargs="*", help='file to graph - you can also pipe data into gauge using "|"')
args = parser.parse_args()

interval = args.i

class Gauge():
    def __init__(self):
        self.screen = Screen()

        f = fileinput.input(args.files)
        if args.f:
            self.read_stream(f)
        else:
            self.read_file(f)

    def read_stream(self, f):
        try:
            line_count = 0
            checkpoint_time = time.time()
            state = State([])
            for _ in f:
                line_count = line_count + 1
                current_time = time.time()
                if (current_time > checkpoint_time + interval):
                    state.add_entry(line_count)

                    if self.screen.is_term_resized():
                        self.screen.resize()

                    self.screen.render(state)

                    line_count = 0
                    checkpoint_time = current_time

        except KeyboardInterrupt:
            self.screen.close()
            f.close()

    def read_file(self, f):
        lines = []
        for line in f:
            lines.append(line)

        state = self.get_state_from_lines(lines)
    
        f.close()

        try:
            while True:
                if self.screen.is_term_resized():
                    self.screen.resize()
                    state = self.get_state_from_lines(lines)
                self.screen.render(state)
                time.sleep(1)
        except KeyboardInterrupt:
            self.screen.close()

    def get_state_from_lines(self, lines):
        groups = {}
        characters = 0
        while len(groups) < self.screen.cols:
            characters = characters + 1
            groups = self.split_into_groups(lines, characters)
            
        sorted_keys = sorted(groups.keys())
        first_key = sorted_keys[0]
        last_key = sorted_keys[-1]
        entries = []

        for key in sorted_keys:
            entries.append(groups[key])

        print("entries: {}".format(entries))
        return State(entries, first_key, last_key)

    def split_into_groups(self, lines, characters):
        groups  = {}
        for line in lines:
            if (line[0].isdigit()):
                group = line[0:characters]
                if group in groups:
                    groups[group] = groups[group] + 1
                else: 
                    groups[group] = 1
        return groups

class State():
    """Class for keeping application state"""
    def __init__(self, entries, first_key="", last_key=""):
        self.entries = entries
        self.y_min = 0
        self.y_max = 0
        self.y_latest = 0
        self.x_min = first_key
        self.x_max = last_key
        self.max_entry = max(entries) if len(entries) else 0

    def add_entry(self, entry):
        self.entries.append(entry)
        self.max_entry = max(self.max_entry, entry)

class Screen():
    """Wrapper for curses screen object"""
    def __init__(self):
        wrapper(self._main)

    def _main(self, cscreen):
        self.cscreen = cscreen # curses screen object
        self.resize()

        curses.noecho()
        curses.curs_set(False)
        curses.cbreak()

    def resize(self):
        self.y, self.x = self.cscreen.getmaxyx()
        self.cscreen.clear()
        curses.resizeterm(self.y, self.x)
        self.cscreen.refresh()
        self.lines = curses.LINES
        self.cols = curses.COLS
        self.screen = [['']*self.cols for _ in range(self.lines)]

    def is_term_resized(self):
        return curses.is_term_resized(self.y, self.x) is True

    def close(self):
        self.cscreen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def render(self, state):
        self._calculate_screen(state)
        self._render_screen(state)

    def _render_screen(self, state): 
        y_max = int(state.max_entry*1.2)
        y_latest = state.entries[-1]
        if state.x_min and state.x_max:
            status = "x=[{}...,{}...] y=[0,{}] y_max={}".format(state.x_min, state.x_max, y_max, state.max_entry)
        else:
            status = "y=[0,{}] i={}s latest={}".format(y_max, interval, y_latest)
        self.cscreen.addstr(0, 0, status)
        for line in range(0, self.lines):
            self._render_line(line, "".join(self.screen[line]))
        self.cscreen.refresh()

    def _render_line(self, line, content):
        self.cscreen.addstr(line, 0, content)

    def _calculate_screen(self, state):
        slice_start = len(state.entries) - self.cols
        slice_end = len(state.entries) - 1

        if slice_start < 0:
            slice_start = 0
                        
        for entry_index in range(slice_start, slice_end):
            entry = state.entries[entry_index]
            col = entry_index - slice_start

            lines4 = self.lines * 4
            normalized_entry = int(entry/(state.max_entry*1.2)*lines4)

            block = "█"
            last_block = self._get_last_block(normalized_entry)

            normalized_entry = normalized_entry // 4

            for line in range(1, self.lines - normalized_entry):
                self.screen[line][col] = ' '
            self.screen[self.lines - normalized_entry - 1][col] = last_block
            for line in range(self.lines - normalized_entry, self.lines):
                self.screen[line][col] = block

    def _get_last_block(self, normalized_entry):
        half_blocks = {
            0: " ",
            1: "▂",
            2: "▄",
            3: "▆"
        }
        return half_blocks[normalized_entry % 4] 

gauge = Gauge()

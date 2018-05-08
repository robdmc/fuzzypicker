#! /usr/bin/env python

import os
import sys
from curses import wrapper
import curses
import textwrap
import argparse
from enum import Enum
from curses import ascii
from fuzzywuzzy import process

class Response(Enum):
    keepon = 1
    escape = 2
    enter = 3




BACKSPACE = 127
ESCAPE = 27
ENTER = 10
UP = {259, 353}
DOWN =  {9, 258}
IGNORED = {260, 261, BACKSPACE, ENTER, ESCAPE}
IGNORED = IGNORED.union(UP)
IGNORED = IGNORED.union(DOWN)



class Color:
    def __init__(self):
        curses.start_color()
        curses.use_default_colors()

        # search_line
        curses.init_pair(1, 253, 17)

        # highlighted
        curses.init_pair(2, 127, -1)

        # footer
        curses.init_pair(3, 240, -1)


    @property
    def search_color(self):
        return curses.color_pair(1)

    @property
    def highlighted(self):
        return curses.color_pair(2)

    @property
    def footer(self):
        return curses.color_pair(3)


class LineCreator:
    def __init__(self, screen):
        self.screen = screen
        self.maxy, self.maxx = self.screen.getmaxyx()

    def draw(self, val, color_pair=None, y=None, x=None):
        val = str(val)
        line_len = self.maxx - 1
        #template = f'{{val: <{line_len}}}'
        #out = template.format(val=val)
        out = f' {val: <{line_len}}'



        if y is None or x is None:
            args = [out]
            #self.screen.addstr('this is a really long line ' * 3, c.cb)
        else:
            args = [y, x, val]
            #self.screen.addstr(y, x, 'this is a really long line ' * 3, c.cb)

        if color_pair:
            args.append(color_pair)

        self.screen.addstr(*args)


class FuzzyPicker:
    def __init__(self, items, default=None, sort_inputs=True):
        items = [str(it) for it in items]
        if sort_inputs:
            self.items = sorted(items)
        else:
            self.items = items

        self.letters = []
        self.highlighted = 0
        self.max_items = 0
        self.selected = None

    def render(self, screen):
        screen.clear()
        curses.curs_set(0)
        maxy, maxx = screen.getmaxyx()
        self.max_items = maxy - 4
        c = Color()
        lc = LineCreator(screen)
        letter_str = ''.join(self.letters)[:maxx-2]
        if not letter_str:
            letter_str = 'Start typing to search'

        if self.letters:
            self.vis_items = process.extract(
                letter_str, self.items, limit=self.max_items)
            self.vis_items = [ii[0] for ii in self.vis_items]
        else:
            self.vis_items = self.items[:self.max_items]

        lc.draw(letter_str, color_pair=c.highlighted)
        lc.draw('')
        for line_num, item in enumerate(self.vis_items):
            if line_num == self.highlighted:
                color_pair = c.search_color
            else:
                color_pair = None
            lc.draw(item[:maxx - 2], color_pair=color_pair)

        lc.draw('(Enter to select. Esc to exit)...', color_pair=c.footer)
        try:
            return screen.getch()
        except KeyboardInterrupt:
            screen.clear()
            sys.exit(0)

    def process(self, key):
        if key == ENTER:
            self.selected = self.vis_items[self.highlighted]
            return Response.enter

        elif key == ESCAPE:
            return Response.escape

        elif key == BACKSPACE and self.letters:
            self.highlighted = 0
            self.letters.pop(-1)
            return Response.keepon

        elif key in UP:
            self.highlighted = max([0, self.highlighted - 1])
            return Response.keepon

        elif key in DOWN:
            self.highlighted = min([self.max_items - 1, self.highlighted + 1])
            return Response.keepon

        elif ascii.isprint(key):
            val = chr(key)
            self.highlighted = 0
            self.letters.append(val)
            return Response.keepon

        else:
            return Response.keepon

    def __call__(self, screen):
        while True:
            key = self.render(screen)
            resp = self.process(key)
            if resp in {Response.escape, Response.enter}:
                break


def create_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

def custom_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 16, 14)

def show_color(screen):
    # From
    # https://stackoverflow.com/questions/18551558/how-to-use-terminal-color-palette-with-curses
    create_colors()
    screen.addstr(0, 0, '{0} colors available'.format(curses.COLORS))
    maxy, maxx = screen.getmaxyx()
    maxx = maxx - maxx % 5
    x = 0
    y = 1
    try:
        for i in range(0, curses.COLORS):
            screen.addstr(y, x, '{0:5}'.format(i), curses.color_pair(i))
            x = (x + 5) % maxx
            if x == 0:
                y += 1
    except: # curses.ERR:
        raise
        pass
    screen.getch()


def picker(lines):
    fp = FuzzyPicker(lines)
    wrapper(fp)
    return fp.selected


if __name__ == '__main__':
    msg = textwrap.dedent('Run command')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    # add a bool argument
    parser.add_argument(
    '-c', '--colors', dest='colors', action='store_true', default=False, help='show colors and exit')

    # get the args
    args = parser.parse_args()

    os.environ.setdefault('ESCDELAY', '25')
    lines = [
        'monkey',
        'donkey',
        'fish',
        'dog',
        'apples',
        'zippers',
        'kites',
        'lemons',
        'monkeys',
        'donkeys',
        'fishes',
        'dogs',
        'apples pie',
        'zip lighters',
        'kite board',
        'lemonaid',
        'wonderful',
        'wives',
        'sister',
        'cough',
        'medicine',
    ]

    if args.colors:
        wrapper(show_color)
    else:
        selected = picker(lines)
        print(f'\n\nselected = {selected!r}')


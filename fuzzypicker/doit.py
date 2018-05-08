#! /usr/bin/env python

from curses import wrapper
import curses
import textwrap
import argparse
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
        curses.init_pair(1, 16, 248)
        curses.init_pair(2, 27, -1)
    @property
    def bk(self):
        return curses.color_pair(2)

    @property
    def kc(self):
        return curses.color_pair(1)


class LineCreator:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.maxy, self.maxx = self.stdscr.getmaxyx()

    def draw(self, val, color_pair=None, y=None, x=None):
        line_len = self.maxx - 1
        #template = f'{{val: <{line_len}}}'
        #out = template.format(val=val)
        out = f' {val: <{line_len}}'



        if y is None or x is None:
            args = [out]
            #self.stdscr.addstr('this is a really long line ' * 3, c.cb)
        else:
            args = [y, x, val]
            #self.stdscr.addstr(y, x, 'this is a really long line ' * 3, c.cb)

        if color_pair:
            args.append(color_pair)

        self.stdscr.addstr(*args)




def main(stdscr):
    c = Color()
    lc = LineCreator(stdscr)
    val = 'hello'
    key = 0
    letters = []
    lines = [
        'first',
        'second',
        'third',
    ]

    highlighted = 0
    do_render = True
    while True:
        stdscr.clear()
        do_render = len(letters)
        if do_render:
            lc.draw(''.join(letters))
            lc.draw('')
            for line_num, line in enumerate(lines):
                if line_num == highlighted:
                    color_pair = c.kc
                else:
                    color_pair = None
                lc.draw(line, color_pair=color_pair)
        lc.draw(str(key))
        key = stdscr.getch()
        val = chr(key)
        if key == BACKSPACE and letters:
            letters.pop(-1)
        elif key == ENTER:
            return
        elif key == ESCAPE:
            stdscr.nodelay(True)
            print('*'*80)
            try:
                stdscr.getch()
            except:
                pass
            return
        elif key in UP and do_render:
            highlighted = max([0, highlighted - 1])
        elif key in DOWN and do_render:
            highlighted = min([len(lines) - 1, highlighted + 1])
        elif key in IGNORED:
            pass
        else:
            letters.append(val)
def create_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

def custom_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 16, 14)

def show_color(stdscr):
    # From
    # https://stackoverflow.com/questions/18551558/how-to-use-terminal-color-palette-with-curses
    create_colors()
    stdscr.addstr(0, 0, '{0} colors available'.format(curses.COLORS))
    maxy, maxx = stdscr.getmaxyx()
    maxx = maxx - maxx % 5
    x = 0
    y = 1
    try:
        for i in range(0, curses.COLORS):
            stdscr.addstr(y, x, '{0:5}'.format(i), curses.color_pair(i))
            x = (x + 5) % maxx
            if x == 0:
                y += 1
    except: # curses.ERR:
        raise
        pass
    stdscr.getch()


if __name__ == '__main__':
    msg = textwrap.dedent('Run command')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    # add a bool argument
    parser.add_argument(
    '-c', '--colors', dest='colors', action='store_true', default=False, help='show colors and exit')

    # get the args
    args = parser.parse_args()

    if args.colors:
        wrapper(show_color)
    else:
        wrapper(main)


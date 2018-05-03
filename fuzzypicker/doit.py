#! /usr/bin/env python

from curses import wrapper
import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    custom_colors()
    #create_colors()
    while True:
        # Clear screen
        stdscr.clear()
        while True:
            nn = 5
            stdscr.addstr(2, 1, f'{curses.color_pair(nn)}', curses.color_pair(nn))
            #stdscr.addstr(2, 1, f'{curses.color_pair(2)}')
            stdscr.getkey()
            #stdscr.refresh()

def create_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

def custom_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(5, 3, 4)
    #for i in range(0, curses.COLORS):
    #    curses.init_pair(i, i, -1)

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


if True:
    wrapper(main)
else:
    wrapper(show_color)

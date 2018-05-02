#! /usr/bin/env python

from curses import wrapper
import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    while True:
        # Clear screen
        stdscr.clear()
        k = 0
        adds = list(range(6))
        while True:
            for i in range(5):
                stdscr.addstr(i+1, 1, f'{curses.color_pair(i)}', 45)
                #stdscr.addstr(i, 0, 'ss' )
            #out = '\n'.join([options[add + k] for add in adds])
            #s = stdscr.getmaxyx()
            #stdscr.addstr(1, 0,str(s), curses.color_pair(3)) 
            #stdscr.addstr(2, 0, out)
            stdscr.refresh()
            stdscr.getkey()
            #k = int(stdscr.getkey(0, 0))


def show_color(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, 56 - 1)
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
    except curses.ERR:
        pass
    stdscr.getch()


if False:
    wrapper(main)
else:
    wrapper(show_color)

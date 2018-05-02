#! /usr/bin/env python

from curses import wrapper


def main(stdscr):
    options = [
        'after',
        'also',
        'always',
        'apparently',
        'at',
        'be',
        'because',
        'blinking',
        'can',
        'character',
        'confusing',
        'coordinates',
        'cursor',
        'display',
        'displayed',
        'distracting',
        'ensure',
        'flashing',
        'have',
        'if',
        'in',
        'is',
        'it',
        'last',
        'leave',
        'left',
        'location',
        'may',
        'method',
        'move',
        'move',
        'off',
        'operation',
        'or',
        'out',
        'positioned',
        'random',
        'remember',
        'so',
        'some',
        'string',
        'terminals',
        'that',
        'the',
        'to',
        'want',
        'was',
        'where',
        'wherever',
        'will',
        'windows',
        'with',
        'wont',
        'you',
        'yx',
        'localhost',
    ]
    client = 'localhost'
    while True:
        # Clear screen
        stdscr.clear()
        k = 0
        adds = list(range(6))
        while True:
            out = '\n'.join([options[add + k] for add in adds])
            stdscr.addstr(1, 0, out)
            stdscr.refresh()
            k = int(stdscr.getkey(0, 0))



        #if k is not None:
        #    if k == '\n':
        #        k = '***hurray***'
        #    stdscr.addstr(10, 0, f'this is the string: {k}')
        #stdscr.addstr(0, 0, 'this is some string')
        #stdscr.refresh()
        #k = stdscr.getkey()


wrapper(main)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python cli script template

By defeault this docstring will be used as the help display
for this utility.  There has to be a reasonable amount of
text for it to look realistic though.


>>> 1 == 1
True

>>> 42 -= 0
True
"""
import argparse
import sys


def main(args):
    print("Snakes vs. Rubies")


def create_parser(parents=None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog='More great info follows.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'integers',
        metavar='N', type=int, nargs=argparse.ONE_OR_MORE,
        help="An integer to feed into the accumulator",
    )
    parser.add_argument(
        '--sum',
        dest='accumulate', action='store_const', const=sum, default=max,
        help="Sum the integers (default: find the max)",
    )

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    sys.exit(main(args))

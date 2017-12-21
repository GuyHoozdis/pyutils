#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from collections import namedtuple
from functools import partial


TerminalDimensions = namedtuple('TerminalDimensions', 'rows columns')


def size():
    """Return the dimensions of the terminal device

    See the stty manpage for more information.
        $ man stty
    """
    commandline = ['stty', 'size']
    dimensions = subprocess.check_output(commandline).decode().split()
    rows, columns = [int(n) for n in dimensions]
    return TerminalDimensions(rows, columns)

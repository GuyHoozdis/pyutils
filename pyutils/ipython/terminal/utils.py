# -*- coding: utf-8 -*-
"""Various utilities and shortcuts that I frequently use within a REPL.
"""
from __future__ import absolute_import, print_function

import json
import traceback

from ipdb import sset_trace
from os import path


def json_load(jsonfile, mode='r', **kwargs):
    """Wrapper around the standard json.load() method.

    This utility merely handles the
    """
    errmsg = "Failed to locate {}."
    assert path.exists(jsonfile), errmsg.format(jsonfile)

    # TODO: Should this catch exceptions?
    with open(jsonfile, mode) as fp:
        data = json.load(fp, **kwargs)

    return data


def json_dump(obj, jsonfile, mode='w', force=False, **kwargs):
    errmsg = "File {} already exists. Set force=True to overwrite."
    assert path.exists(jsonfile) and not force, errmsg.format(jsonfile)

    # TODO: Should this catch exceptions?
    with open(jsonfile, mode) as fp:
        json.dump(obj, fp, **kwargs)


def step_into(entrypoint, *args, **kwargs):
    """Step into any executable object with ipdb.

    Use this from a shell, like iPython or the standard REPL, to arbitrarily
    step into any executable code that is loaded in the terminal.
    """
    assert callable(entrypoint), (
        "Entrypoint {} is not callable!  That's going to be an issue."
    ).format(entrypoint)

    sset_trace()
    return entrypoint(*args, **kwargs)


# These are the command definitions that used to be in my .pdbrc file.
#
# ```
# alias trace locals()['frame']=[frame for frame in traceback.extract_stack() \
#    if os.path.basename(frame[0]).startswith("test_")][0]
# alias print_trace print traceback.format_list([locals()["frame"]])[0]
# ```
#
#
# The port isn't working yet...
# -----------------------------------------------------------------------------
# ipdb> from pyutils.ipython.terminal.utils import which_test
# ipdb> which_test
# <function which_test at 0x106577cf8>
# ipdb> which_test()
# *** ValueError: too many values to unpack
# ipdb>
# -----------------------------------------------------------------------------
def which_test():
    #locals()['frame'] = [
    frames_with_prefix_test = [
        frame for frame in traceback.extract_stack()
        if path.basename(frame[0]).startswith("test_")
    ]
    assert frames_with_prefix_test, "Failed to locate any candidate frames"

    # TODO: I just transformed what used to be two commands in .pdbrc into this
    # single command, but I haven't actually tried to use it yet.
    tbdata = traceback.format_list(frames_with_prefix_test[0])
    print(tbdata[0])

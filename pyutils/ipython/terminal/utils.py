# -*- coding: utf-8 -*-
"""Various utilities and shortcuts that I frequently use within a REPL.
"""
from __future__ import absolute_import, print_function

import json
import traceback

from os import path


json_loads = json.loads
json_dumps = json.dumps


def json_load(jsonfile, mode='r', **kwargs):
    """Wrapper around the standard json.load() method.

    This utility merely handles the
    """
    errmsg = "Failed to locate {}."
    assert path.exists(jsonfile), errmsg.format(jsonfile)

    with open(jsonfile, mode) as fp:
        data = json.load(fp, **kwargs)

    return data


def json_dump(obj, jsonfile, mode='w', force=False, **kwargs):
    errmsg = "File {} already exists. Set force=True to overwrite."
    file_exists = path.isfile(jsonfile)
    if file_exists and not force:
        raise Exception(errmsg.format(jsonfile))

    config = dict([('default', str),], **kwargs)
    with open(jsonfile, mode) as fp:
        json.dump(obj, fp, **config)


def step_into(entrypoint, *args, **kwargs):
    """Step into any executable object with ipdb.

    Use this from a shell, like iPython or the standard REPL, to arbitrarily
    step into any executable code that is loaded in the terminal.
    """
    assert callable(entrypoint), (
        "Entrypoint {} is not callable!  That's going to be an issue."
    ).format(entrypoint)

    import ipdb; ipdb.sset_trace();  # Breakpoint
    return entrypoint(*args, **kwargs)


def which_test():
    """Find the most recent calling test on the stack.
    """
    frames_with_prefix_test = [
        frame for frame in traceback.extract_stack()
        if path.basename(frame[0]).startswith("test_")
    ]
    assert frames_with_prefix_test, "Failed to locate any candidate frames"

    # TODO:
    # - Return an object instead of printing a string or maybe optionally
    #   return an object instead of printing.
    # - Take parameters on how to format rendered output.
    # - Wrap some of the elements with utilities (e.g. Parse the basename,
    #   relative path, or ... out of the first element.
    tbdata = traceback.format_list(frames_with_prefix_test)
    print(tbdata[0])

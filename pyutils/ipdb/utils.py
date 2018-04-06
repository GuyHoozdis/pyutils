# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

import json
from ipdb import sset_trace


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

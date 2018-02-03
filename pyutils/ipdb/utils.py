from __future__ import absolute_import


def step_into(entrypoint, *args, **kwargs):
    """Step into any executable object with ipdb
    """
    assert callable(entrypoint), (
        "Entrypoint {} is not callable!  That's going to be an issue."
    ).format(entrypoint)

    import ipdb; ipdb.sset_trace();  # XXX: Breakpoint
    return entrypoint(*args, **kwargs)

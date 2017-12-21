# ##########################################################################
# I am trying to get a breakpoint in Alembic, but I'm not getting my prompt
# on stdout.  Alembic doesn't offer switches like `pytest` or `nosetests` do,
# so I'm going to try this out.
#
#   https://github.com/gotcha/ipdb/issues/105#issuecomment-245638752
# ##########################################################################
from inspect import getargspec
from ipdb.__main__ import def_colors, def_exec_lines
from IPython import version_info as ipython_version
from IPython.terminal.interactiveshell import TerminalInteractiveShell


def _get_debugger_cls():
    if ipython_version < (5, 0, 0):
        from IPython.core.debugger import Pdb
        return Pdb
    return TerminalInteractiveShell().debugger_cls


#def _init_pdb(context=3, commands=[]):
def _init_pdb(context=3):
    debugger_cls = _get_debugger_cls()
    if 'context' in getargspec(debugger_cls.__init__)[0]:
        p = debugger_cls(def_colors, context=context)
    else:
        p = debugger_cls(def_colors)
    p.rcLines += def_exec_lines
    #p.rcLines.extend(commands)
    return p


def patch_ipdb():
    """

    Example:

        from pyutils.ipdb import patch_ipdb; patch_ipdb().sset_trace();  # Break
    """
    import ipdb
    ipdb.__main__._init_pdb = _init_pdb
    return ipdb

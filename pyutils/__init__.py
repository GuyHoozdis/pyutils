# -*- coding: utf-8 -*-
"""Personal PythonUtility Library
"""
from __future__ import absolute_import
from __future__ import print_function

import collections
import functools
import itertools
import operator

from pyutils.terminal.autostatus import AutoStatusUpdateGenerator
from pyutils.terminal.format.prepr import ppd, ppl, pi, ppsql
from pyutils.terminal.format.cprint import cformat, cprint
from pyutils.tradecraft import nt_from_dict, trace_factory
from pyutils.tradecraft.datastructures import ChainMap
from pyutils.tradecraft.decorators import inspect_method
from pyutils.tradecraft import footilities
from pyutils.tradecraft.loggers import log_with
from pyutils.tradecraft.testutils import DecimalEncoder, dump_docs


Utilities = collections.namedtuple('Utilities', 'description utilities')

data_inspection = Utilities(
    "Object inspection utilities",
    ('ppd', 'ppl', 'pi', 'ppsql', 'dump_docs',)
)
io_utilities = Utilities(
    "Logging, output, and data dump helpers",
    ('cformat', 'cprint', 'log_with', 'trace_factory', 'DecimalEncoder',)
)
data_structures = Utilities(
    "Data structures and factories",
    ('ChainMap', 'nt_from_dict',)
)
fooiter = Utilities(
    "All the itertools",
    tuple([util for util in dir(footilities) if not util.startswith('_')])
)


__all__ = ['footilities'] + [
    util for util in itertools.chain(
        data_inspection.utilities,
        data_structures.utilities,
        io_utilities.utilities,
        data_structures.utilities,
    )
]


AutoStatus = StatusGenerator = AutoStatusUpdateGenerator

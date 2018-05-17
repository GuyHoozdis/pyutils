# -*- coding: utf-8 -*-
"""Personal PythonUtility Library
"""
from __future__ import absolute_import
from __future__ import print_function

import collections
import functools
import itertools
import operator

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


## Just eff-ing around
try:
    import factory
except ImportError:
    def autostatus_updates(*providers, **kwargs):
        return "Could not import 'factory'.  Have you installed it?"
else:
    from collections import Iterator, namedtuple
    from operator import methodcaller

    class AutoStatusUpdateGenerator(collections.Iterator):
        _default_providers = ['catch_phrase', 'bs']
        _default_template = "I am working on {a_or_an} {0}, so that we can {1}"

        @property
        def template(self):
            return self.__template

        @template.setter
        def template(self, value):
            self.__template = value

        @property
        def providers(self):
            return self.__providers

        def generate(self, **kwargs):
            assert self.providers, "No data providers have been configured"
            content = map(methodcaller('generate', kwargs), self.providers)
            assert content, "No content was generated by the data providers"
            a_or_an = 'an' if content[0][0].lower() in 'aeiou' else 'a'

            return self.template.format(*content, a_or_an=a_or_an)

        def next(self):
            return self.generate()

        def __init__(self, *providers, **kwargs):
            self.__template = kwargs.get('template', self._default_template)
            providers = providers if providers else self._default_providers
            self.__providers = nt_from_dict('DataProviders', **{
                provider: factory.Faker(provider)
                for provider in providers
            })

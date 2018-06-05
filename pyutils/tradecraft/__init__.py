# -*- coding: utf-8 -*-
from __future__ import absolute_import

import contextlib
import logging
import io
import string

from collections import namedtuple


def nt_from_dict(name='Namespace', **kwargs):
    """
    """
    items = kwargs.items()
    keys, values = zip(*items)
    return namedtuple(name, keys)(*values)


def nt_from_list(name='Namespace', transform=string.upper, *values):
    transform = lambda x: x if transform is None else transform
    assert callable(transform), "The transform parameter must be callable"
    data = {transform(v): v for v in values}
    return nt_from_dict(**data)


@contextlib.contextmanager
def trace_factory(ostream=None, logger_name='factory', loglevel=logging.DEBUG):
    """A context manager for examining the internals of FactoryBoy factories.

    >>> with trace_factory() as monitor:
    ...     some_object = SomeObjectFactory()
    ...     # ...
    ...
    >>> lines = monitor.ostream.getvalue()
    """
    factory_logger = logging.getLogger(logger_name)
    previous_loglevel = factory_logger.level
    ostream = ostream if ostream is not None else io.StringIO()
    handler = logging.StreamHandler(ostream)
    handler.setLevel(loglevel)
    factory_logger.addHandler(handler)
    factory_logger.setLevel(loglevel)

    yield namedtuple("DebugOutput", 'logger ostream')(factory_logger, file)

    factory_logger.setLevel(previous_loglevel)
    factory_logger.removeHandler(handler)

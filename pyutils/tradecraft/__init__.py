# -*- coding: utf-8 -*-
from __future__ import absolute_import

import contextlib
import logging
import io
import itertools
import string

from collections import namedtuple


def nt_from_dict(name='Namespace', **kwargs):
    """Create a mapping contained within this constrained scope.
    """
    items = kwargs.items()
    keys, values = zip(*items)
    return namedtuple(name, keys)(*values)


def nt_from_list(*values, **meta):
    """Given an iterable collection of values,

    >>> import decimal, string
    >>> nt_from_list('ios', 'android', name='Platform', transform=string.upper)
    Platform(IOS='ios', ANDROID='android')

    >>> nt_from_list(
            '10', '100', '1000', '10000',
            name='LogScale',
            transform="L{}".format,
            value_type=decimal.Decimal,
        )
    LogScale(L10=Decimal('10'), L100=Decimal('100'), L1000=Decimal('1000'))
    """
    name = meta.get('name', 'Enumeration')
    transform = meta.get('transform', string.upper)
    value_type = meta.get('value_type', unicode)

    # TODO:
    # - Allow the iterable `values` to be a list key-value pairs
    # - If `value_type` is explicitly given as `None`, then do not change
    # - If `transform` is explicitly given as `None`, then do not change
    name_error = "The 'name' parameter must be a non-empty string value"
    assert name and isinstance(name, basestring), name_error
    assert callable(transform), "The transform parameter must be callable"
    assert callable(value_type), "The value_type must be a constructor"

    items = [(transform(v), value_type(v)) for v in values]
    keys, values = zip(*items)
    return namedtuple(name, keys)(*values)


@contextlib.contextmanager
def trace_factory(ostream=None, logger_name='factory', loglevel=logging.DEBUG):
    """A context manager for examining the internals of FactoryBoy factories.

    >>> with trace_factory() as monitor:
    ...     some_model = SomeModelFactory()
    ...     # ...
    ...
    >>> lines = monitor.ostream.getvalue()

    >>> ostream = open('output.log', 'a+')
    >>> with trace_factory(ostream=ostream) as monitor:
    ...     some_model = SomeModelFactory()
    ... ostream.close()
    """
    factory_logger = logging.getLogger(logger_name)
    previous_loglevel = factory_logger.level
    ostream = ostream if ostream is not None else io.StringIO()
    handler = logging.StreamHandler(ostream)
    handler.setLevel(loglevel)
    factory_logger.addHandler(handler)
    factory_logger.setLevel(loglevel)

    yield namedtuple("DebugOutput", 'logger ostream')(factory_logger, ostream)

    factory_logger.setLevel(previous_loglevel)
    factory_logger.removeHandler(handler)

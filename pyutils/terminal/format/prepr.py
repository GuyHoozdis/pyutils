# -*- coding: utf-8 -*-
"""REPL shell utility methods to aid debugging/inspection of data structures

Functions
---------
pi()
    TODO: Give the deets

ppl()
    TODO: Give the deets

ppd()
    TODO: Give the deets

ppsql()
    TODO: Give the deets
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import re
import sys

from os import path
from collections import namedtuple
from pprint import pprint
from six import iteritems

try:
    import sqlparse
except ImportError:
    sqlparse = None

from .cprint import cprint



def pi(instance, pattern=None, show_hidden=False, **kwargs):
    """Print instance attributes and a repr of its value

    By default, any attribute that starts with "_" or "__" is not shown.  Set
    show_hidden=True, when calling this method, to show them.

    Use the pattern parameter to create a regex which then be used to identify
    which attributes will be shown.

    The method dynamically calculates allotted space for the attributes values
    and instead of wrapping, truncates the attribute value representation.  The
    maximum space available for attribute values is determined by the current
    console columns minus the max length of the attribute names/keys minus some
    padding.  All aspects of formatting can be overriden through the following
    parameters:

    key_value_sep   - Symbol used to separate key from value.
    key_width       - Reserved space for displaying key.
    value_precision - The max width for displaying attribute values.
    """
    if not hasattr(instance, '__dict__') or len(instance.__dict__) == 0:
        raise ValueError("Instance has no readable attributes")

    key_pattern = re.compile(pattern) if pattern else None
    def show_attribute(name):
        """A filter function to determine if an attribute will be shown"""
        if not key_pattern:
            is_hidden = name.startswith('_')
            return not is_hidden or (is_hidden and show_hidden)
        return True if key_pattern.search(name) else False

    def determine_console_dimensions():
        try:
            dimensions = os.popen('stty size', 'r').read()
            height, width = map(int, dimensions.split())
        except:
            height, width = 0, 0
        return namedtuple('ConsoleDimensions', 'height width')(height, width)

    def determine_format_kwargs():
        console = determine_console_dimensions()
        key_width = max([a.keylen for a in attributes])
        key_value_sep = kwargs.get('key_value_sep', ' = ')
        value_precision = console.width - key_width - len(key_value_sep)
        format_kwargs = {
            'key_width': key_width,
            'key_value_sep': key_value_sep,
            'value_precision': value_precision if value_precision > 0 else 80,
        }
        format_kwargs.update(kwargs)
        return format_kwargs

    attributes = sorted([
        namedtuple('AttributeInfo', ['name', 'value', 'keylen'])(k, v, len(k))
        #for k, v in instance.__dict__.iteritems() if show_attribute(k)
        for k, v in iteritems(instance.__dict__) if show_attribute(k)
    ])
    if len(attributes) == 0:
        raise ValueError("No instance attributes met display criteria")

    format_kwargs = determine_format_kwargs()
    format_line = "{:>{key_width}}{key_value_sep}{:.{value_precision}}".format
    for attribute in attributes:
        format_args = [attribute.name, repr(attribute.value)]
        print(format_line(*format_args, **format_kwargs))


def ppsql(query, chartype=str, file=sys.stdout, **overrides):
    """Pretty print SQL statements

    query       - A string of SQL or SQLAlchemy query object
    chartype    - unicode, str, or ...
    file        - Anything that exposes a .write() method
    overrides   - Override the options passed to sqlparse.format()
    """
    if not sqlparse:
        cprint(
            "{color.red}Requires sqlparse module to be installed{color.stop}",
            file=sys.stderr
        )
        return
    options = dict(reindent=True, keyword_case='upper')
    options.update(**overrides)
    statement = query.statement.compile(compile_kwargs={"literal_binds": True})
    try:
        formatted_statement = sqlparse.format(chartype(statement), **options)
    except Exception as ex:
        msg = "{color.red}Failed to bind literals; {color.cyan}{}{color.stop"
        cprint(msg, ex, file.sys.stderr)
        formatted_statement = sqlparse.format(chartype(query), **options)
    print(formatted_statement, file=file)


def ppl(obj):
    pprint(list(obj))


def ppd(obj):
    pprint(dict(obj))



# TODO:
# - Add `ppd` and `ppl` convenience methods
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys

# TODO: This is being replaced by the method "pi".  After it has shown to be
# working properly, this can be removed.  2017/11/28
def print_instance(instance, show_hidden=False, key_len=None):
    key_value_sep = ' = '
    format_member = (
        "{:>{key_precision}}{key_value_sep}{:{value_precision}.{value_precision}}"
    ).format

    _, columns = os.popen('stty size', 'r').read().split()
    def _calculate_precision(attr_name, key_len):
        value_len = int(columns) - (key_len + len(key_value_sep)) - 1
        value_len = value_len - len(attr_name) if len(attr_name) > key_len else value_len
        return {
            'key_precision': key_len,
            'value_precision': value_len,
            'key_value_sep': key_value_sep,
        }

    for attr_name in sorted(instance.__dict__.keys()):
        if attr_name.startswith('_') and not show_hidden:
            continue
        attr_value = repr(instance.__dict__[attr_name])
        # TODO: Use a fixed length for now (instead of respecting)
        fixed_key_len = 20 if key_len is None else key_len
        precision = _calculate_precision(attr_name, key_len=fixed_key_len)
        msg = format_member(attr_name, attr_value, **precision)
        print(msg)


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
    import re
    from collections import namedtuple
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
        for k, v in instance.__dict__.iteritems() if show_attribute(k)
    ])
    if len(attributes) == 0:
        raise ValueError("No instance attributes met display criteria")

    format_kwargs = determine_format_kwargs()
    format_line = "{:>{key_width}}{key_value_sep}{:.{value_precision}}".format
    for attribute in attributes:
        format_args = [attribute.name, repr(attribute.value)]
        print(format_line(*format_args, **format_kwargs))


# TODO:
# - I don't recall why I had to switch the default from unicode to str, but
#   that could probably be done in a more generic way.
#def ppsql(query, chartype=unicode, ostream=sys.stdout, **overrides):
def ppsql(query, chartype=str, ostream=sys.stdout, **overrides):
    """Pretty print SQL statements

    query       - A string of SQL or SQLAlchemy query object
    chartype    - unicode, str, or ...
    ostream     - Anything that exposes a .write() method
    overrides   - Override the options passed to sqlparse.format()
    """
    try:
        import sqlparse
    except ImportError:
        sys.stderr.write("Requires sqlparse module to be installed\n")
        return
    try:
        from sqlalchemy.sql import compiler
    except ImportError:
        sys.stderr.write("Requires sqlalchemy to be installed\n")
        return

    options = dict(reindent=True, keyword_case='upper')
    options.update(overrides)

    formatted_statement = sqlparse.format(chartype(query.statement), **options)
    ostream.write(formatted_statement + '\n')

    # TODO: Trying to render SQL with parameters
    #dialect = query.session.bind.dialect
    #statement = query.statement
    #comp = compiler.SQLCompiler(dialect, statement)
    #comp.compile()
    #enc = dialect.encoding
    #params = {}
    #for k, v in comp.params.iteritems():
    #    if isinstance(v, unicode):
    #        v.encode(enc)
    #    params[k] = v
    #statement_with_params = (comp.string.encode(enc) % params).decode(enc)
    #formatted_statement = sqlparse.format(
    #    chartype(statement_with_params), **options)
    #ostream.write(formatted_statement + '\n')


def json_load(jsonfile):
    import json
    from os import path
    assert path.exists(jsonfile), "Failed to locate {}".format(jsonfile)

    # TODO: This should catch exceptions that occur when file is not JSON
    with open(jsonfile) as fp:
        data = json.load(fp)
    return data

# -*- coding: utf-8 -*-
"""Colorized formatting and printing of text streams.

TODO:
    - Replace the OrderedDict collections with custom classes that derive
      from ``enum.Enum``
    - Implement ``Napolean Sphinx documentation plugin``_.


.. _Napolean Sphinx documentation plugin:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
"""
from __future__ import absolute_import, print_function

import collections
import sys
from six import iteritems

try:
    from itertools import izip as zip
except ImportError:
    pass


__all__ = ['cformat', 'cprint']


NIL = 0

TEXT_STYLES  = collections.OrderedDict([
    ('bold', 1),
    ('dark', 2),
    ('underline', 4),
    ('blink', 5),
    ('reverse', 7),
    ('concealed', 8),

    ('stop', NIL),
])

FOREGROUND_COLORS = collections.OrderedDict([
    ('grey', 30),
    ('red', 31),
    ('green', 32),
    ('yellow', 33),
    ('blue', 34),
    ('magenta', 35),
    ('cyan', 36),
    ('white', 37),

    ('stop', NIL),
])

BACKGROUND_COLORS = collections.OrderedDict([
    ('on_grey', 40),
    ('on_red', 41),
    ('on_green', 42),
    ('on_yellow', 43),
    ('on_blue', 44),
    ('on_magenta', 45),
    ('on_cyan', 46),
    ('on_white', 47),

    ('stop', NIL),
])



def __format_terminal_code(code):
        return "\033[{:d}m".format(code)


def __make_terminal_code(codes, classname='TerminalCodes'):
    #(keys, values) = zip(*codes.iteritems())
    (keys, values) = zip(*iteritems(codes))
    return collections.namedtuple(classname, keys)(*[
        __format_terminal_code(value) for value in  values
    ])


__TERMINAL_CODES = collections.OrderedDict([
    #('bg', background),
    #('bgnd', background),
    #('background', background),
    ('bg', __make_terminal_code(BACKGROUND_COLORS)),

    #('fg', colors),
    #('fgnd', colors),
    #('foreground', colors),
    ('color', __make_terminal_code(FOREGROUND_COLORS)),

    ('style', __make_terminal_code(TEXT_STYLES)),

    #('reset', NIL),
    #('stop', NIL),
    #('nil', NIL),
    #('stop', __format_terminal_code(NIL)),
])


def cformat(template, *args, **kwargs):
    """Colorized and styled formatting

    >>> tmpl = "{color.red}This is very {}!{color.stop}"
    >>> cformat(tmpl, "concerning")
    '\x1b[31mThis is very concerning!\x1b[0m'
    >>> print(cformat(tmpl, "important"))
    This is very important!
    """
    kwargs.update(**__TERMINAL_CODES)
    return template.format(*args, **kwargs)


def cprint(template, sep=' ', end='\n', file=sys.stdout, *args, **kwargs):
    """Format colorized template and write to a stream

    >>> tmpl = "{color.red}This is very {}!{color.stop}"
    >>> cprint(tmpl, "impressive")
    This is very impressive!
    """
    message = cformat(template, *args, **kwargs)
    print(message, sep=sep, end=end, file=file)


# TODO: Not sure this is the best place for this... just need it now.
import functools
def print_marker(message, *args, **kwargs):
    default_marker_template = (
        "{color.red}{style.bold}MARKER{style.stop}"
        "{color.white}: "
        "{color.green}{message}{color.stop}"
    )
    sep = kwargs.pop('sep', ' ')
    end = kwargs.pop('end', '\n')
    file = kwargs.pop('file', sys.stdout)
    marker_template = kwargs.pop('marker_template', default_marker_template)
    format_marker = functools.partial(pyutils.cformat, marker_template)

    msg = message.format(*args, **kwargs)
    mark = marker_template(message=msg)
    print(mark, file=sys.stderr)


# I think I might like this better than the method.
# TODO:
# - Give the ability to render with or without color.
# - Stack / traceback info
# - Be a breakpoint?  Mark somewhere, run, exception happens, next run breaks
#   before exception... idk... pretty dreamy.
class IOStreamMarker(object):
    _default_marker_template = (
        "{color.red}{style.bold}MARKER{style.stop}"
        "{color.white}: "
        "{color.green}{message}{color.stop}"
    )

    def __init__(self, *args, **kwargs):
        self.sep = kwargs.pop('sep', ' ')
        self.end = kwargs.pop('end', '\n')
        self.ostream = kwargs.pop('file', sys.stdout)
        self.marker_template = kwargs.pop(
            'marker_template',
            self._default_marker_template
        )

    def __call__(self, message, *args, **kwargs):
        sep = kwargs.pop('sep', self.sep)
        end = kwargs.pop('end', self.end)
        ostream = kwargs.pop('file', self.ostream)

        msg = message.format(*args, **kwargs)
        mark = cformat(self.marker_template, message=msg)
        print(mark, sep=sep, end=end, file=ostream)

def demo():
    import os
    from pprint import pformat

    def print_banner(message):
        template = '{color.green}{bg.on_red}{style.bold}{message}{stop}'
        banner = cformat(template, message=message)
        print(banner)


    print_banner("Declaring MyMeta")


    class MyMeta(type):
        message_template = {
            'footer': '{color.red}{style.dark}{marker}{newlines}{stop}',
            'allocate': (
                '{color.green}{style.underline}Allocating memory for class:{stop} '
                '{color.magenta}{classname}{stop}'),
            'initialize': (
                '{color.green}{style.underline}Initializing class:{stop} '
                '{color.magenta}{classname}{stop}'),
            'attribute': (
                '{color.red}{label:<6}{stop} = {color.magenta}{value}{stop}'),
            'invoke': (
                '{color.green}{style.underline}Invoking class:{stop} '
                '{color.magenta}{classname}{stop}'),
        }

        @classmethod
        def _print_formatted_message(cls, template_name, *args, **kwargs):
            template = cls.message_template[template_name]
            message = cformat(template, *args, **kwargs)
            print(message)

        @staticmethod
        def _format_attribute(value, indention=2, **kwargs):
            formatted_value = pformat(value, indent=indention)
            if isinstance(value, dict) and len(value) > 1:
                formatted_value = (
                    formatted_value[0] + os.linesep
                    + ' ' * indention + formatted_value[2:-1] + os.linesep
                    #+ ' ' * (indention - 1)
                    + formatted_value[-1]
                )
            return formatted_value

        def __new__(meta, name, bases, body):
            meta._print_formatted_message('allocate', classname=name)
            for label, value in [('meta', meta), ('bases', bases), ('body', body)]:
                formatted_value = meta._format_attribute(value)
                attribute = dict(label=label, value=formatted_value)
                meta._print_formatted_message('attribute', **attribute)
            meta._print_formatted_message('footer', marker='='*40, newlines='\n')
            return super(MyMeta, meta).__new__(meta, name, bases, body)

        def __init__(cls, name, bases, body):
            cls._print_formatted_message('initialize', classname=name)
            for label, value in [('class', cls), ('bases', bases), ('body', body)]:
                formatted_value = cls._format_attribute(value)
                attribute = dict(label=label, value=formatted_value)
                cls._print_formatted_message('attribute', **attribute)
            cls._print_formatted_message('footer', marker='='*40, newlines='\n\n')
            super(MyMeta, cls).__init__(name, bases, body)

        def __call__(cls, *args, **kwargs):
            cls._print_formatted_message('invoke', classname=cls)
            cls._print_formatted_message(
                'attribute',
                label='args',
                value=cls._format_attribute(args),
            )
            cls._print_formatted_message(
                'attribute',
                label='kwargs',
                value=cls._format_attribute(kwargs),
            )
            cls._print_formatted_message('footer', marker='='*40, newlines='\n')
            return type.__call__(cls, *args, **kwargs)


    print_banner("Declaring MyClass")

    class MyClass(MyMeta):
        pass


    print_banner("Instantiating MyClass")
    myclass = MyClass()

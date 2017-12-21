#!/usr/bin/env python2
"""
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import collections
import textwrap

import termcolor

from functools import partial
from pprint import pformat
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name


ATTRIBUTES, COLORS, HIGHLIGHTS = [
    collections.namedtuple(classname, keys)(*[
        "\033[{:d}m".format(value) for value in values
    ])
    for classname, (keys, values) in [
        (name[:-1].lower().capitalize(),
            zip(*getattr(termcolor, name).items()))
        for name in ['ATTRIBUTES', 'COLORS', 'HIGHLIGHTS']
    ]
]


COLOR_CODES = collections.OrderedDict([
    ('bkgnd', HIGHLIGHTS),
    ('color', COLORS),
    ('style', ATTRIBUTES),
    ('stop', termcolor.RESET),
])


def cformat(template, *args, **kwargs):
    """Colorized and styled formatting
    """
    kwargs.update(**COLOR_CODES)
    return template.format(*args, **kwargs)

def wrap(text, **override):
    class indent(object):
        space = ' '
        tab = '\t'
        def __init__(self, n): self._n = n
        def get_tabs(self): return self._n * self.tab
        def get_spaces(self): return self._n * self.space
        tabs = property(get_tabs)
        spaces = property(get_spaces)

    #indent = '  '
    #indention = lambda n: indent * n

    kwargs = dict(
        width=80,
        expand_tabs=True,
        replace_whitespace=True,
        drop_whitespace=False,
        #initial_indent=indention(3),
        #subsequent_indent=indention(3),
        initial_indent=indent(3).spaces,
        subsequent_indent=indent(3).spaces,
    )
    kwargs.update(**override)

    return textwrap.wrap(text, **kwargs)


def print_banner(message):
    template = '{color.green}{bkgnd.on_red}{style.bold}{message}{stop}'
    banner = cformat(template, message=message)
    print(banner)


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


def run_demo():
    """Demonstrate MyMeta's invocation.

    When MyKlass, or any class that uses MyMeta, is read, then MyMeta is
    invoked.
    """
    print_banner('Declaring an object that uses the metaclass')
    class MyKlass(object):
        __metaclass__ = MyMeta
        attribute = 2

        def __init__(self, *args, **kwargs):
            self._args = args
            self._kwargs = kwargs

        def method(self, variable=None):
            return 42 // (variable if variable is not None else self.attribute)

    print_banner("Instantiating the class invokes __call__ on the metaclass")
    myklass = MyKlass('Tesla', 42, should_raise=False)


if __name__ ==  '__main__':
    run_demo()

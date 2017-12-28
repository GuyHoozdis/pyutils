#!/usr/bin/env python2
"""Support colorized formatting and printing of text streams.

Functions
---------

cformat()
    TODO: give the deets

cprint()
    TODO: give the deets
"""
from __future__ import absolute_import
from __future__ import print_function

import collections
import sys


__all__ = ['cformat', 'cprint']


TEXT_STYLES  = collections.OrderedDict([
    ('bold', 1),
    ('dark', 2),
    ('underline', 4),
    ('blink', 5),
    ('reverse', 7),
    ('concealed', 8)
])

FOREGROUND_COLORS = collections.OrderedDict([
    ('grey', 30),
    ('red', 31),
    ('green', 32),
    ('yellow', 33),
    ('blue', 34),
    ('magenta', 35),
    ('cyan', 36),
    ('white', 37)
])

BACKGROUND_COLORS = collections.OrderedDict([
    ('on_grey', 40),
    ('on_red', 41),
    ('on_green', 42),
    ('on_yellow', 43),
    ('on_blue', 44),
    ('on_magenta', 45),
    ('on_cyan', 46),
    ('on_white', 47)
])

NIL = 0


def __format_terminal_code(code):
        return "\033[{:d}m".format(code)


def __make_terminal_code(codes, classname='TerminalCodes'):
    (keys, values) = zip(*codes.iteritems())
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
    ('stop', __format_terminal_code(NIL)),
])


def cformat(template, *args, **kwargs):
    """Colorized and styled formatting
    """
    kwargs.update(**__TERMINAL_CODES)
    return template.format(*args, **kwargs)


def cprint(template, sep=' ', end='\n', file=sys.stdout, *args, **kwargs):
    """Format colorized template and write to a stream
    """
    message = cformat(template, *args, **kwargs)
    print(message, sep=sep, end=end, file=file)


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

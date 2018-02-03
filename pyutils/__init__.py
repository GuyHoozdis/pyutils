# -*- coding: utf-8 -*-
from __future__ import absolute_import


__all__ = [
    # REPL/iPDB console utilities
    'ppd', 'ppl', 'pi', 'ppsql',

    # Colorized terminal output
    'cformat', 'cprint',

    # Debugging helper
    'tracer',
]


# REPL/iPDB console utilities
from pyutils.terminal.format.prepr import ppd, ppl, pi, ppsql
# Colorized terminal output
from pyutils.terminal.format.cprint import cformat, cprint
#
from pyutils.tradecraft.decorators import *
#
#from pyutils.ipdb.utils import *




## Just eff-ing around
try:
    import factory
except ImportError:
    def autostatus_updates(*providers, **kwargs):
        return "Could not import 'factory'.  Have you installed it?"
else:
    from collections import OrderedDict
    def auto_status_updates(*providers, **kwargs):
        default_providers = ['catch_phrase', 'bs']
        default_template = "I am working on {0}, so that we can {1}"

        template = kwargs.get('template', default_template)
        providers = providers if providers else default_providers
        data_providers = OrderedDict([
            factory.Faker(provider) for provider in providers
        ])
        get_data_from_provider = operator.methodcaller('generate', {})

        def generate(**context):
            return template.format(
                *map(get_data_from_provider, providers.values()),
                **context
            )




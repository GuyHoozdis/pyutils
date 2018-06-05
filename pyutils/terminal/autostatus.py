# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from collections import Iterator, namedtuple
from operator import methodcaller

from pyutils.terminal.format.cprint import cformat, cprint
from pyutils.tradecraft import nt_from_dict


try:
    import factory
except ImportError as err:
    cprint(
        "{color.white}{bg.on_red}{style.concealed}"
        "Could not import 'factory'. Is it installed?"
        "{color.stop}"
    )
    raise err


class AutoStatusUpdateGenerator(Iterator):
    _default_providers = ['catch_phrase', 'bs']
    _default_template = "I am working on {a_or_an} {0}, so that we can {1}."

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


def initialize_generator(*providers, **kwargs):
    status_generator = AutoStatusUpdateGenerator(*providers, **kwargs)
    return status_generator.generate


generate = initialize_generator()


if __name__ == "__main__":
    print(cformat("{color.green}{}{color.stop}", generate()))
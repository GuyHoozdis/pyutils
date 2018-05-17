from __future__ import absolute_import
from __future__ import print_function

import functools
import logging


#log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


class log_with(object):
    """Logging decorator

    Wrap functions, object methods, or whole classes and log the activity
    >>> logging.basicConfig()
    >>> log = logging.getLogger('custom_log')
    >>> log.setLevel(logging.DEBUG)
    >>> log.info('what up!')

    >>> print("Prior to decling/wrapping method foo.")
    >>> @log_with(log)
    >>> def foo():
    ...     print("So, this is what it feels like to be inside foo.")
    >>> print("Prior to invoking foo()")
    >>> foo()
    >>> print("After invoking foo")

    >>> print("Next declare foo2, but use a default logger")
    >>> @log_with()
    >>> def foo2():
    ...     print("I'm in foo too")

    >>> print("You were about to call me?  I was about to call foo 2")
    >>> foo2()
    >>> print("Do you work on clases too?")
    >>> @log_with(log)
    >>> class Foo(object):
    ...     def __init__(x, y=0): self._x, self._y = x, y
    ...     def bar(self): return self._y / 0
    ...     def baz(cls): return self._x / self._y
    ...     baz = classmethod(baz)
    ...     x = property('_x')

    >>> bar, baz = Foo(5), Foo(4, 0)
    >>> bar.x, baz.baz, baz.bar()

    """
    format_entry_message = "Entering: {.__name__}".format
    format_exit_message = "Exiting: {.__name__}".format

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        """Returns a wrapper that can deocrate functions and log entry/exit

        The wrapper logs at the INFO level by default.
        """
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        # BUG: See `TODO.md` in the project's root directory.
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug(self.format_entry_message(func))
            f_result = func(*args, **kwargs)
            self.logger.debug(self.format_exit_message(func))
            return f_result
        return wrapper



if __name__ == "__main__":
    from os import environ
    loglevel = environ.get('PYUTILS_LOG_LEVEL', 'INFO')

    logging.basicConfig()
    log = logging.getLogger(__name__)
    log.setLevel(loglevel)


    def banner(text='', template="\n{:-^40}\n"):
        print(template.format(text))


    [getattr(log, attribute)("[!] Logging level activated")
     for attribute in ['critical', 'error', 'warn', 'info', 'debug']]


    #print("\n{:-^40}\n".format("Decorating Methods"))
    banner("Decorating Methods")
    print("[*] Prior to decling/wrapping method foo.")
    @log_with(log)
    def foo():
        print("[-] So, this is what it feels like to be inside foo.")

    print("[*] Prior to invoking foo()")
    foo()
    print("[*] After invoking foo")

    print("[*] Next declare foo2, but use a default logger")
    @log_with()
    def foo2():
        print("[-] I'm in foo too")

    print("[*] You were about to call me?  I was about to call foo 2")
    foo2()


    banner("Decorating Classes")
    print("[*] Do you work on clases too?")
    @log_with(log)
    class Foo(object):
        _x, _y = 22, 7

        # XXX: The decorator doesn't handle properties properly.
        #x = property(_x)
        #y = property(_y)

        def __init__(self, x, y=0):
            self._x, self._y = x, y

        def bar(self):
            return self._y / 0

        @classmethod
        def baz(cls):
            return self._x / self._y

        def x(self):
            return self._x


    bar = Foo(5)
    baz = Foo(4, 0)
    bar.x
    baz.baz
    #bar, baz = Foo(5), Foo(4, 0)
    #bar.x, baz.baz, baz.bar()

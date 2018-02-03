from __future__ import absolute_import
from __future__ import print_function
import functools
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class log_with(object):
    """Logging decorator
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

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug(self.format_entry_message(func))
            f_result = func(*args, **kwargs)
            self.logger.debug(self.format_exit_message(func))
            return f_result
        return wrapper



if __name__ == "__main__":
    logging.basicConfig()
    log = logging.getLogger('custom_log')
    log.setLevel(logging.DEBUG)
    log.info('what up!')

    print("Prior to decling/wrapping method foo.")

    @log_with(log)
    def foo():
        print("So, this is what it feels like to be inside foo.")
    print("Prior to invoking foo()")
    foo()
    print("After invoking foo")


    print("Next declare foo2, but use a default logger")
    @log_with()
    def foo2():
        print("I'm in foo too")

    print("You were about to call me?  I was about to call foo 2")
    foo2()

    print("Do you work on clases too?")

    @log_with(log)
    class Foo(object):
        def __init__(x, y=0): self._x, self._y = x, y
        def bar(self): return self._y / 0
        def baz(cls): return self._x / self._y
        baz = classmethod(baz)
        x = property('_x')

    bar, baz = Foo(5), Foo(4, 0)
    bar.x, baz.baz, baz.bar()

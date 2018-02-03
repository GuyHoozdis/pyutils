# TODO: Just throwing this in here for the moment..
# This is a more developed concept of a similar utility. The trace has been
# handy so far.
#   http://code.activestate.com/recipes/577551-trace-decorator-for-debugging/
import sys
import inspect
from pprint import pformat
from pyutils import cformat, cprint
from decorator import decorator

@decorator
def tracer(f, *args, **kwargs):
    argspec = inspect.getargspec(f)
    callargs = inspect.getcallargs(f, *args, **kwargs)
    args_with_defaults = argspec[0][-len(argspec[3]):]
    format_named_vars = "  - {0:<15} = {1!r}".format
    header  = [
        " {color.cyan}## Method Context ######## {color.stop}",
        cformat((
            " ====={color.magenta} Name{color.stop}: {style.bold}{color.green}"
            "{0.__name__}{color.stop}"
        ), f),
    ]
    namedvars_lines = [
        " ===== {color.magenta}Named vars{color.stop} ==========="
    ] + [
        format_named_vars(name, callargs[name]) for name in argspec[0]
    ]
    varargs_lines = [" ===== {color.magenta}*varargs{color.stop} ===========",]
    if not callargs[argspec[1]]:
        varargs_lines += [format_named_vars(argspec[1], '(, )'),]
    else:
        varargs_lines += [
            format_named_vars(argspec[1], value)
            for value in callargs[argspec[1]]
        ]
    kwargs_lines = [
        " ===== {color.magenta}**kwargs{color.stop} ============",
    ] + [format_named_vars(argspec[2], '{'+pformat(callargs[argspec[2]])+'}' ) ]
    footer = [ " ----------------------- ", ]

    cprint('\n'.join(
        header + namedvars_lines + varargs_lines + kwargs_lines + footer
    ), file=sys.stderr)
    print("Args & defaults:", zip(args_with_defaults, argspec[3]))
    return f(*args, **kwargs)




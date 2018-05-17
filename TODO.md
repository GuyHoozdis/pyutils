# Next

As soon as there is free time, these should be done or will have
the biggest impact if they were done now.


# Soon

Not the highest priority, but more useful sooner than later.


## File Header

Get the common file header or start new files from template...


## Snippet Search

Search certain collections of example code for keywords, tags, ...


# Some day

I don't know when I'll get to these, but if there is nothing else to do or suddenly the
idea becomes more relevant, then it gets queued up.


## Log Marker

Output easy to fine log messages when there is a deluge of log output.
- Markers add context to the log output that immediately follows
- Markers can be in color for console use
- Markers can be without escape codes / colors in log files - grepable
- Optionally include frame / stack info

```python
import pyutils, functools
format_marker = functools.partial(pyutils.cformat, (
    "{color.red}{style.bold}MARKER{style.stop}"
    "{color.white}: "
    "{color.green}{message}{color.stop}"
))
def print_marker(message, *args, **kwargs):
    msg = message.format(*args, **kwargs)
    mark = format_marker(message=msg)
    print(mark)
```



## Decorating SqlAlchemy class with `log_with` debugging utility causes error


SqlAlchemy has a lot of indirection.  It appears that at one point they are trying
to inspect the decorated class and aren't getting access to an attribute that is
assumed to exist.

This utility should be transparent when it is applied.

Before trying to fix the decorator, see if something similar can be acomplished by
using the `mock` library creating a spy.

_See the entrypoint for some examples of ways that this goes wrong._

```
Traceback (most recent call last):
  File "tools/interactive_app.py", line 143, in <module>
    sys.exit(main())
  File "tools/interactive_app.py", line 139, in main
    return embed_shell(args)
  File "tools/interactive_app.py", line 112, in embed_shell
    shell_locals = _prepare_embeded_shell_namespace(config)
  File "tools/interactive_app.py", line 79, in _prepare_embeded_shell_namespace
    from pos_api import controllers, models, resources, run_app, schemas, settings
  File "/Users/sully/Development/union/backend/pos_api/run_app.py", line 4, in <module>
    from pos_api.app import create_app, settings
  File "/Users/sully/Development/union/backend/pos_api/app/__init__.py", line 22, in <module>
    from pos_api.resources import (
  File "/Users/sully/Development/union/backend/pos_api/resources/dashboard/__init__.py", line 8, in <module>
    from pos_api.resources.dashboard.labor import LaborHoursResource
  File "/Users/sully/Development/union/backend/pos_api/resources/dashboard/labor.py", line 19, in <module>
    from pos_api.schemas.dashboard import LaborSchema
  File "/Users/sully/Development/union/backend/pos_api/schemas/__init__.py", line 97, in <module>
    class ScreenSchema(Schema):
  File "/Users/sully/Development/union/backend/pos_api/schemas/__init__.py", line 105, in ScreenSchema
    size = field_for(models.Screen, 'size', field_class=fields.Str)
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/marshmallow_sqlalchemy/convert.py", line 149, in field_for
    prop = model.__mapper__.get_property(property_name)
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/mapper.py", line 1919, in get_property
    configure_mappers()
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/mapper.py", line 3029, in configure_mappers
    mapper._post_configure_properties()
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/mapper.py", line 1831, in _post_configure_properties
    prop.post_instrument_class(self)
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/interfaces.py", line 544, in post_instrument_class
    self.strategy.init_class_attribute(mapper)
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/dynamic.py", line 41, in init_class_attribute
    query_class=self.parent_property.query_class,
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/strategies.py", line 106, in _register_attribute
    **kw
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/attributes.py", line 1509, in register_attribute_impl
    impl = impl_class(class_, key, typecallable, dispatch, **kw)
  File "/Users/sully/.pyenv/versions/union-backend-recovery/lib/python2.7/site-packages/sqlalchemy/orm/dynamic.py", line 61, in __init__
    elif AppenderMixin in query_class.mro():
AttributeError: 'log_with' object has no attribute 'mro'
make[2]: *** [interactive] Error 1
```

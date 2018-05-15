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

# PyUtils

A collection of scripts that I use frequently and would like to share/reuse.  This
functionality is more about my workflow and common tasks agnostic of any specific 
project.

Until I can figure out the organization that works best, I just made this directory
a package.  I didn't want to duplicate the folder name `pyutils/pyutils`, but I do
want to give a namespace hint when I import logic from here. 

For example; When I use the `ShellPrompts` class from an `ipython_config.py` file 
I think it would be better to be doing this 

    from pyutils.path.to.prompts import ShellPrompts
    c.Terminal

than what I was doing right before I added `__init__.py` to this directory).


## Organization

I have more questions than answers at this point.  Working with the `format_curl.py`
and a symbolic link from `~/bin` has worked well for me.  I need to put other things
that I do frequently in there (e.g. generating my union instances ssh config file or
installing the configuration I like into instances).


How should I manage these modules/packages?  A single repo?  No repo?  Individual repos
and then use a requirements file to install the packages?

- [Namespace packaging][namespace-packaging] might be solution to the questions above!
- Hosting my own [index server][package-index] could be another.
- Installing from development mode, archive files, or repos are options too.


[namespace-packaging]: https://packaging.python.org/guides/packaging-namespace-packages/
[package-index]: https://packaging.python.org/guides/index-mirrors-and-caches/

## Scenarios

As more usage scenarios arise, I will describe them here.


### iPython utils / helpers

TODO: ...  


[ipyhon-demo]: http://ipython.readthedocs.io/en/stable/interactive/reference.html#interactive-demos-with-ipython

#### The Shell Profile

TODO: ...  


#### Prompt customization

My custom shell prompts... TODO


#### Re-implement `%rehashx`

The default implementation imports things it shouldn't (e.g shims from the
`<pyenv-root>/bin` directory).  I might be able to modify the $PATH variable
before executing %rehash.  [Re-implementing][custom-magic] the command, or a
similar concept with a name variation, would be interesting too.

The existing `%rehashx` magic is defined in `ipython/core/magics/osm.py`; see
either the source code `~/Development/github/ipython` or any site-packages
installation to find `osm.py`.


[custom-magic]: http://ipython.readthedocs.io/en/5.x/config/custommagics.html#defining-magics

#### Aliases from ipdb

I like them so much I'd like to have them availabl in normal ipython shells
too.


#### Start-up directories

Is this a good way to leverage code that I want available in terminals?  I
can't put things needed for configuration in there, but I could put other
things.  Maybe my startup files should be a link out of the startup directory
to a module shared with ipdbrc.


### LoDash Port

I love the `lodash` library.  It would be fun to port that functionality 
into a python package.  These `itertools` [receipies][itertools-receipes] 
would be a good start though.


[itertools-receipes]: https://docs.python.org/3/library/itertools.html#recipes

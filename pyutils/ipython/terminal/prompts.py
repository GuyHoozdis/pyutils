import os
import subprocess
from collections import namedtuple
from IPython.terminal.prompts import Prompts, Token
from six import iteritems

# LazyEvaluate
#
# This approach didn't work for me... what's up with his syntax for the return
# in parse_git_branch()?  I just want to leave this for reference.  There might
# be something to the Lazy approach.
#
#   https://gist.github.com/jseabold/3442688
#
#from IPython.core.prompts import LazyEvaluate


# TODO: Define and document the config options.  For now, just play it loose
# and grab everything that is prefixed with `IPYSH_`.
#
# Here are some ideas about implementing configuration.
#
# - https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
# - https://12factor.net/config
#
# IPYSH_DISABLE - Default: Not set
#   If defined, the custom prompt will not be attached as the `prompt_class`
#   for the terminal's instance.  It would be possible to manually assign a
#   `prompt_class`, but removing this value from the environment won't re-
#   enable it.
#
# IPYSH_ABBRV_HOME - Default: True
#   Replace the current directory with `~` if the current path is starts with
#   the user's home directory.  The value of $HOME is read from the env vars
#   When the terminal is initialized.  Changing the env var value will not
#   will not affect running instances of the terminal.
#
# IPYSH_PATH_DEPTH - Default None
#   Similar to BASH's feature to limit the path output to the last n path
#   components.  This value is read during initialization.
#
# IPYSH_TOKENS_STACKED - Default "stacked"
#   A limited set of choices on how to lay out the components, which are:
#   - stacked: One prompt token per line, with the terminal prompt on its
#     own line.
#   - horozontal: A single line for the prompt tokens, with the terminal prompt
#     on its own line.
#   - oneline: A single line.
#   - off: Don't display anything other than the terminal prompt.
#
# IPYSH_TERMINAL_PROMPT - Default "ipysh> "
#


# !!!: This is terrible.  Only allowable while it is only me using this code.
# An attacker could inject code through env vars. If allowing this to be
# configurable ends up being useful, then implement a legitimate config parser.
def _string_to_native(string_value):
    try: return eval(string_value)
    except NameError, SyntaxError:
        return self.ERROR


# To go beyond the dumb polling that is happening here, perhaps it would be
# effective to leverage file-system events.  I think pyinotify is older.
# There is a package called `watchdog` that installs a command-line
# `watchmedo` that is partially based on the code from MacFSEvnts.
#
# - https://github.com/seb-m/pyinotify (every ohter url is about the same package - MacFSEvents)
# - https://pypi.python.org/pypi/MacFSEvents
# - https://github.com/malthe/macfsevents
# - https://blog.philippklaus.de/2011/08/watching-directories-for-changes-using-python_-_an-overview/
# - https://blog.philippklaus.de/2011/08/use-the-python-module-macfsevents-to-monitor-directories-for-changes-on-mac-os-x/
#
# I didn't come across this until later.  It is pretty simple, but it might be
# a useful reference.
#
#   https://gist.github.com/takluyver/85b33db0836cdcc4baf252fd81937fa7
#
class ShellPrompt(Prompts):
    ERROR = 'ERROR'

    OFF = 'off'
    ONELINE = 'oneline'
    HORIZONTAL = 'horizontal'
    STACKED = 'stacked'
    LAYOUT_OPTIONS = (OFF, ONELINE, HORIZONTAL, STACKED)

    BRANCH = 'Branch'
    PYENV = 'PyEnv'
    APPENV = 'AppEnv'
    LABELS = dict(
        branch=BRANCH,
        pyenv=PYENV,
        appenv=APPENV,
    )

    # XXX: Am I going to need this?
    #State = namedtuple('State', ['location', 'branch'])
    defaults = dict(
        IPYSH_ABBREV_HOME=True,
        IPYSH_PATH_DEPTH=None,
        IPYSH_TERMINAL_PROMPT="ipysh> ",
        IPYSH_TOKEN_LAYOUT=STACKED,
    )

    virtualenv = None
    home = None
    config = None

    def __init__(self, *args, **kwargs):
        super(ShellPrompt, self).__init__(*args, **kwargs)
        self._read_config()
        self.home = os.getenv('HOME', self.ERROR)
        self.virtualenv = subprocess.Popen(
            args='venv=$(pyenv version-name); echo "${venv//:/|}"',
            shell=True,
            stdout=subprocess.PIPE,
        ).communicate()[0].strip() or self.ERROR

    def _read_config(self, force=False):
        if force or not self.config:
            self.config = self.defaults.copy()
            self.config.update({
                key: _string_to_native(value)
                for key, value in iteritems(os.environ)
                if key.startswith('IPYSH_') and '' != value.strip()
            })

    #def _read_state(self, force=False):
    #    # XXX: Maybe I should have used the decorator package and memoized
    #    # a fuction that does this work.
    #    previous = next(self._state, None)
    #    if force or not previous:
    #        location = os.getcwd()
    #        branch = _git_current_branch()
    #        self._state = itertools.repeat(
    #            self.State(
    #            )
    #        )
    #    return next(self._state)

    def _prepare_current_directory_token(self, depth=None, abbrev_user=True):
        """Format the current directory for display.

        If depth is an integer greater than 0, then that value will be used
        to slice the tail elements of the current directory.

        If abbrev_user is True, the user's home directory will be abbreviated
        with a tilde.
        """
        cwd = os.getcwd()
        abbrev_user = self.config.get('IPYSH_ABBREV_HOME', abbrev_user)
        if abbrev_user and self.home and cwd.startswith(self.home):
            cwd = cwd.replace(self.home, '~', 1)

        depth = self.config.get('IPYSH_PATH_DEPTH', depth)
        if depth and depth < cwd.count(os.sep):
            elements = cwd.split(os.sep)[-depth:]
            cwd = os.sep.join(['...'] + elements)

        return cwd

    def _prepare_current_branch_token(self):
        # TODO: This is actually executing on every key press, but it doesn't
        # seem to be interfereing with the user experience, so I'm leaving it
        # for now.
        return subprocess.Popen(
            args=(
                "branch=$(git branch --no-color 2> /dev/null | grep '^\* '); "
                "echo \"${branch#* }\""
            ),
            shell=True,
            stdout=subprocess.PIPE,
        ).communicate()[0].strip() or " ---------- "

    def _prepare_current_venv_token(self):
        # XXX: There are a few problems with this approach.
        # - This method is invoked on every key-press and that makes the
        #   terminal response feel choppy.  It doesn't need to be checked
        #   that often.  It could be dumply after any command execution or
        #   more intelligently after certain events.
        # - Reading the PYENV_VERSION is initially correct.  It doesn't
        #   noticably slow down the interaction, but it doesn't need to to
        #   query the value on each key press.
        # - !!!: What does it mean to swich virtual environments from within
        #   a ipython shell that was started from another enironment.
        # ----------------------------------------------------------------
        #if not self.virtualenv:
        #    self.virtualenv = subprocess.Popen(
        #        args='venv=$(pyenv version-name); echo "${venv//:/|}"',
        #        shell=True,
        #        stdout=subprocess.PIPE,
        #    ).communicate()[0].strip()
        return self.virtualenv if self.virtualenv else "Error"

    def in_prompt_tokens(self, cli=None):
        # TODO: I'm not yet using the self._read_state() to be more efficient
        # and only make calls, like os.getcwd() or os.getenv(), once per
        # invocation of this method (i.e. when two different tokens use the
        # same value, don't let them both make system calls).
        return list(reversed([t for t in self.token_layout_generator()]))

    def token_layout_generator(self):
        """Iterating will produce the prompt tokens in reverse order.

        The IPYSH_ config variables dictate how the stream of tokens
        should be constructed.  Once the generator is exhausted, the
        resulting list must be reversed before being returned.
        """
        tfs_space, tfs_newline = ' ', os.linesep
        yield (Token.Prompt, self.config['IPYSH_TERMINAL_PROMPT'])

        layout = self.config['IPYSH_TOKEN_LAYOUT']
        if layout not in self.LAYOUT_OPTIONS:
            layout = self.defaults['IPYSH_TOKEN_LAYOUT']
        if layout == self.OFF:
            raise StopIteration
        elif layout == self.ONELINE:
            yield (Token, tfs_space)
        else:
            yield (Token, tfs_newline)

        token_sep = tfs_newline if layout == self.STACKED else tfs_space
        format_label = '{:{width}} : '.format
        width = max([len(label) for label in self.LABELS.itervalues()])

        # Current Dicrectory
        yield (Token.Prompt, ']')
        yield (Token, self._prepare_current_directory_token())
        yield (Token.Prompt, '[')

        # Git Branch
        yield (Token, token_sep)
        yield (Token.Prompt, ')')
        yield (Token, self._prepare_current_branch_token())
        #yield (Token.Prompt, '(Branch: ' )
        yield (Token.Prompt, format_label('Branch', width=width))
        yield (Token.Prompt, '(' )

        # Python Virtual Environment
        yield (Token, token_sep)
        yield (Token.Prompt, ')')
        yield (Token, self._prepare_current_venv_token())
        #yield (Token.Prompt, '(PyEnv: ' )
        yield (Token.Prompt, format_label('PyEnv', width=width))
        yield (Token.Prompt, '(' )

        # Application Environment
        yield (Token, token_sep)
        yield (Token.Prompt, ')')
        yield (Token, os.environ.get('APP_ENVIRONMENT', 'System'))
        yield (Token.Prompt, format_label('AppEnv', width=width))
        yield (Token.Prompt, '(' )

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from pyutils import cformat, cprint
from pyutils.terminal import autostatus


## Just eff-ing around  :-P
if __name__ == "__main__":
    status_message = cformat(
        "{color.green}{}{color.stop}",
        autostatus.generate()
    )
    print(status_message)

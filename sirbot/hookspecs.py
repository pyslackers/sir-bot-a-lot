"""
Hookspecs of the core plugins
"""

import pluggy

hookspec = pluggy.HookspecMarker('sirbot')


@hookspec
def plugins(loop):
    pass  # pragma: no cover

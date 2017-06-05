"""
Hookspecs of the core plugins
"""

import pluggy

hookspec = pluggy.HookspecMarker('sirbot')


@hookspec
def plugins(loop):
    """
    Hook for registering a plugin.

    Args:
        loop (asyncio.AbstractEventLoop): Event loop

    Returns:
        sirbot.core.plugin.Plugin: A plugin instance
    """
    pass  # pragma: no cover

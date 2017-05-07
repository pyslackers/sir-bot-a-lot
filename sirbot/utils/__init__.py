import asyncio
import logging
import functools

main_logger = logging.getLogger(__name__)


def merge_dict(a, b, path=None):
    """
    Merge dict b into a
    """
    if not path:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            else:
                continue
        else:
            a[key] = b[key]
    return a


def ensure_future(coroutine, loop=None, logger=None):
    logger = logger or main_logger
    callback = functools.partial(error_callback, logger=logger)
    future = asyncio.ensure_future(coroutine, loop=loop)
    future.add_done_callback(callback)


def error_callback(f, logger):
    try:
        error = f.exception()
    except asyncio.CancelledError:
        return

    if error is not None:
        logger.exception("Task exited with error",
                         exc_info=error)

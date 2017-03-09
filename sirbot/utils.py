import asyncio
import logging
import functools

main_logger = logging.getLogger('sirbot')


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

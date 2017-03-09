import asyncio

from sirbot.utils import ensure_future


async def test_ensure_future(loop, capsys):
    coro = raise_error(loop=loop)
    ensure_future(coro, loop=loop)
    await asyncio.sleep(0.2, loop=loop)
    out, err = capsys.readouterr()
    assert 'Task exited with error' in err
    assert 'ValueError' in err


async def test_ensure_future_cancel(loop, capsys):
    coro = cancel(loop=loop)
    ensure_future(coro, loop=loop)
    await asyncio.sleep(0.2, loop=loop)
    out, err = capsys.readouterr()
    assert '' in err


async def raise_error(loop):
    await asyncio.sleep(0.1, loop=loop)
    raise ValueError

async def cancel(loop):
    await asyncio.sleep(0.1, loop=loop)
    raise asyncio.CancelledError

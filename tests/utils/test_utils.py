import asyncio

from sirbot.utils import ensure_future, merge_dict


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


def test_merge_dict():
    a = {"a": 1, "b": [2, 3], "c": {"x": 1, "y": [2, 3], "z": {}}}
    b_ok = {"a": 1, "b": [2, 3], "c": {"x": 1, "y": [2, 3], "z": {}}}
    c_ok = {"a": 1, "b": [4, 5], "c": {"x": 1, "y": [2, 3], "z": {}}}

    b = {}
    b = merge_dict(b, a)
    assert b == b_ok

    c = {"b": [4, 5], "c": {"x": 1}}
    c = merge_dict(c, a)
    assert c == c_ok

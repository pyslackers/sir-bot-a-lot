import uuid

import pytest


@pytest.fixture(scope='function', autouse=True)
def patch_current_loop(loop, monkeypatch):
    monkeypatch.setattr('asyncio.get_event_loop', lambda: loop)


@pytest.fixture(scope='function')
def token():
    return str(uuid.uuid4())

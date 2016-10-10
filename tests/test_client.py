import uuid

import pytest

from sirbot.client import _APICaller
from sirbot.errors import (
    SlackAPIError,
    SlackRedirectionError,
    SlackConnectionError,
    SlackServerError,
)


class MockClientResponse:
    def __init__(self, *args, status=200, json=None, **kwargs):
        self._status = status
        self._json = json

    @property
    def status(self):
        return self._status

    async def json(self):
        return self._json

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        pass


async def test_apicaller_post_response_ok(loop, monkeypatch, token):
    """Validates the handling of 200 status codes with an ok slack response"""
    resp_json = dict(ok=True, id=str(uuid.uuid4()))
    monkeypatch.setattr('sirbot.client.aiohttp.ClientSession.post',
                        lambda *args, **kwargs: MockClientResponse(json=resp_json))  # noqa

    caller = _APICaller(token, loop=loop)
    resp = await caller._do_post('foobar')
    assert resp['id'] == resp_json['id']


async def test_apicaller_post_response_not_ok(loop, monkeypatch, token):
    """Validates the handling of 200 status codes, but with a slack response
    of not ok"""
    resp_json = dict(ok=False)
    monkeypatch.setattr('sirbot.client.aiohttp.ClientSession.post',
                        lambda *args, **kwargs: MockClientResponse(json=resp_json))  # noqa

    caller = _APICaller(token, loop=loop)
    with pytest.raises(SlackAPIError):
        await caller._do_post('foobar')


@pytest.mark.parametrize('status, err', [
    (300, SlackRedirectionError),
    (302, SlackRedirectionError),
    (399, SlackRedirectionError),
    (400, SlackConnectionError),
    (499, SlackConnectionError),
    (500, SlackServerError),
    (599, SlackServerError),
])
async def test_apicaller_post_redirect_handling(status, err, loop, monkeypatch, token):
    """Validates the handling of erroring status codes"""
    monkeypatch.setattr('sirbot.client.aiohttp.ClientSession.post',
                        lambda *args, **kwargs: MockClientResponse(status=status))
    caller = _APICaller(token, loop=loop)
    with pytest.raises(err):
        await caller._do_post('foobar')


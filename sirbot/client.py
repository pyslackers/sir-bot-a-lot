import asyncio
import json
import logging
from urllib.parse import urlencode

import aiohttp

from .base import Channel
from .queue import IterableQueue

logger = logging.getLogger('sirbot')


class SlackClientError(Exception):
    """Generic slack client error"""


class SlackConnectionError(SlackClientError):
    """Connection to slack server error"""


class SlackServerError(SlackClientError):
    """Internal slack server error"""


class SlackRedirectionError(SlackClientError):
    """Redirection status code"""


class SlackAPIError(SlackClientError):
    """Wrong use of slack API"""


class HTTPClient:
    def __init__(self, token, *, loop=None):
        self.api_root = 'https://slack.com/api/{0}'
        self.api_post_msg = self.api_root.format('chat.postMessage')
        self.api_update_msg = self.api_root.format('chat.update')
        self.api_delete_msg = self.api_root.format('chat.delete')
        self.api_add_react = self.api_root.format('reactions.add')
        self.api_delete_react = self.api_root.format('reactions.remove')
        self.api_get_react = self.api_root.format('reactions.get')
        self.api_get_channel = self.api_root.format('channels.list')
        self.api_get_channel_info = self.api_root.format('channels.info')
        self.token = token
        self.session = aiohttp.ClientSession()
        self.loop = loop or asyncio.get_event_loop()

    def __del__(self):
        if not self.session.closed:
            self.session.close()

    async def delete(self, message):
        """
        Delete a previously sent message

        :param message: Message previously sent
        :type message: Message
        :return: Timestamp of the message
        """
        logger.debug('Message Delete: {}'.format(message))
        msg = self._prepare_message(message)
        rep = await self._query_api(msg, self.api_delete_msg)
        return rep.get('ts')

    async def send(self, message):
        """
        Send a new message

        :param message: Message to send
        :type message: Message
        :return: Timestamp of the message
        """
        logger.debug('Message Sent: {}'.format(message))
        url = self.api_post_msg
        msg = self._prepare_message(message)
        rep = await self._query_api(msg, url)
        return rep.get('ts')

    async def update(self, message, timestamp=None):
        """
        Update a previously sent message

        If no timestamp if provided we assumed the timestamp of the previous
        message is stored in the new message. This enable the update of a
        message without creating a new message.

        :param message: New message
        :param timestamp: Timestamp of the message to update
        :return: Timestamp of the message
        """
        logger.debug('Message Update: {}'.format(message))
        url = self.api_update_msg
        msg = self._prepare_message(message, timestamp)
        rep = await self._query_api(msg, url)
        return rep.get('ts')

    def _prepare_message(self, message, timestamp=None):
        """
        Format the message for the Slack API

        :param message: Message to send/update/delete
        :param timestamp: Timestamp of the message
        :return: Formatted msg
        :rtype: dict
        """
        msg = message.serialize()
        msg['token'] = self.token
        if timestamp:
            msg['ts'] = timestamp

        return msg

    async def _query_api(self, msg, url):
        """
        Query the Slack API and check the response for error.

        :param msg: payload to send
        :param url: url for the request
        :type msg: dict
        :return: Slack API Response
        :rtype: dict
        """
        async with self.session.post(url, data=msg) as response:
            if 200 <= response.status < 300:
                rep = await response.json()
                if rep['ok'] is True:
                    logger.debug('Message API response: {}'.format(rep))
                    return rep
                else:
                    logger.warning('Message API response: {}'.format(rep))
                    raise SlackAPIError(rep)
            elif 300 <= response.status < 400:
                e = 'Redirection, status code: {}'.format(response.status)
                logging.error(e)
                raise SlackRedirectionError(e)
            elif 400 <= response.status < 500:
                e = 'Client error, status code: {}'.format(response.status)
                logging.error(e)
                raise SlackConnectionError(e)
            elif 500 <= response.status < 600:
                e = 'Server error, status code: {}'.format(response.status)
                raise SlackServerError(e)

    async def add_reaction(self, message, reaction='thumbsup'):
        """
        Add a reaction to a message

        See Slack API documentation and team settings for available reaction

        :param message: Message to add reaction to
        :param reaction: Reaction to add
        """
        msg = self._prepare_reaction(message, reaction)
        logger.debug('Reaction Add: {}'.format(msg))
        await self._query_api(msg, self.api_add_react)

    async def delete_reaction(self, message, reaction):
        """
        Delete a reaction from a message

        :param message: Message to delete reaction from
        :param reaction: Reaction to delete
        """
        msg = self._prepare_reaction(message, reaction)
        logger.debug('Reaction Delete: {}'.format(msg))
        await self._query_api(msg, self.api_delete_react)

    async def get_reaction(self, message):
        """
        Query all the reactions of a message

        :param message: Message to query reaction from
        :return: List of dictionary with the reaction name, count and users
        as keys
        :rtype: list
        """
        msg = self._prepare_reaction(message)
        msg['full'] = True  # Get all the message information
        logger.debug('Reaction Get: {}'.format(msg))
        rep = await self._query_api(msg, self.api_get_react)
        return rep.get('message').get('reactions')

    def _prepare_reaction(self, message, reaction=''):
        """
        Format the message and reaction for the Slack API

        :param message: Message to add/delete/get reaction
        :param reaction: Reaction to add/delete
        :return: Formatted message
        :rtype: dict
        """
        msg = message.serialize()
        msg['token'] = self.token
        msg['name'] = reaction
        msg['timestamp'] = msg['ts']
        return msg

    async def get_channels(self):
        """
        Query all available channels in the teams and identify in witch
        channel the bot is present.

        :return: two list of channels. First one contain the channels where the
        bot is present. Second one contain all the available channels of the
        team.
        """
        logging.debug('Getting channels')
        all_channels = []
        bot_channels = []

        msg = {'token': self.token}
        rep = await self._query_api(msg, self.api_get_channel)
        for chan in rep.get('channels'):
            channel = Channel(channel_id=chan['id'], **chan)
            all_channels.append(channel)
            if chan.get('is_member'):
                bot_channels.append(channel)

        return bot_channels, all_channels

    async def get_channels_info(self, channel_id):
        """
        Query the information about a channel

        :param channel_id: id of the channel to query
        :return: information
        :rtype: dict
        """
        msg = {
            'token': self.token,
            'channel': channel_id
        }

        rep = await self._query_api(msg, self.api_get_channel_info)
        return rep['channel']


class RTMClient:
    def __init__(self, token, *, loop=None):
        self.ws = None
        self.loop = loop or asyncio.get_event_loop()
        self.api_root = 'https://slack.com/api/{0}'
        self.message_id = 0
        self.token = token
        self.queue = IterableQueue()
        self.session = aiohttp.ClientSession()
        self._login_data = None
        self._closed = asyncio.Event(loop=self.loop)

    def __del__(self):
        if not self.session.closed:
            self.session.close()

    @property
    def is_closed(self):
        """bool: Indicates if the websocket connection is closed."""
        return self._closed.is_set()

    async def api_call(self, method='?', post_data=None):
        post_data = post_data or {}
        post_data['token'] = self.token
        post_data = urlencode(post_data).encode()

        url = self.make_api_url(method)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }

        async with self.session.post(url, data=post_data,
                                     headers=headers) as resp:
            if resp.status != 200:
                logger.error('Unable to post to slack: %s', await resp.text())
                raise SlackConnectionError('Slack connection error')
            return await resp.json()

    def make_api_url(self, method):
        return self.api_root.format(method)

    async def rtm_connect(self, reconnect=False):
        try:
            method = 'rtm.start'
            self._login_data = await self.api_call(method)

            if self._login_data.get('ok') is False:
                raise SlackConnectionError(
                    'Error with slack {}'.format(self._login_data))

            ws_url = self._login_data['url']
            async with self.session.ws_connect(ws_url) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        msg = json.loads(msg.data)
                        await self.queue.put(msg)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break  # noqa
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break  # noqa
        except asyncio.CancelledError:
            pass

    async def send_message(self, message, method='send', *args, **kwargs):
        if method == 'update':
            logger.warning('RTMClient does not support message update')
        data = {
            'type': 'message',
            'channel': message.to.id,
            'text': message.text
        }
        logger.debug('Message Sent: {}'.format(message))
        await self.ws.send(json.dumps(data))

    def run(self):
        try:
            self.loop.run_until_complete(self.rtm_connect())
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()

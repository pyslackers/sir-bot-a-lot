import asyncio
import json
import logging
from typing import Any, AnyStr, Dict, Optional

import aiohttp

from .base import Channel, Message, User
from .errors import (
    SlackConnectionError,
    SlackServerError,
    SlackRedirectionError,
    SlackAPIError
)

logger = logging.getLogger('sirbot')


class _APIPath:
    """Path definitions for slack"""
    SLACK_API_ROOT = 'https://slack.com/api/{0}'

    ADD_REACT = SLACK_API_ROOT.format('reactions.add')
    DELETE_MSG = SLACK_API_ROOT.format('chat.delete')
    DELETE_REACT = SLACK_API_ROOT.format('reactions.remove')
    GET_CHANNEL = SLACK_API_ROOT.format('channels.list')
    GET_CHANNEL_INFO = SLACK_API_ROOT.format('channels.info')
    GET_REACT = SLACK_API_ROOT.format('reactions.get')
    POST_MSG = SLACK_API_ROOT.format('chat.postMessage')
    RTM_START = SLACK_API_ROOT.format('rtm.start')
    UPDATE_MSG = SLACK_API_ROOT.format('chat.update')


class _APICaller:
    """
    Helper class for anything that can call the slack API.

    :param token: Slack API Token
    :param loop: Asyncio event loop to run in.
    """
    __slots__ = ('_token', '_loop', '_session')

    def __init__(self, token: str, *,
                 loop: Optional[asyncio.BaseEventLoop]=None):
        self._token = token
        self._loop = loop or asyncio.get_event_loop()
        self._session = aiohttp.ClientSession(loop=self._loop)

    def __del__(self):
        if not self._session.closed:
            self._session.close()

    async def _do_post(self, url: str, *,
                       msg: Optional[Dict[AnyStr, Any]]=None,
                       token: Optional[AnyStr]=None):
        """
        Perform a POST request, validating the response code.
        This will throw a SlackAPIError, or decendent, on non-200
        status codes

        :param url: url for the request
        :param msg: payload to send
        :param token: optionally override the set token.
        :type msg: dict
        :return: Slack API Response
        :rtype: dict
        """
        msg = msg or {}
        msg['token'] = token or self._token
        async with self._session.post(url, data=msg) as response:
            if 200 <= response.status < 300:
                rep = await response.json()
                if rep['ok'] is True:
                    logger.debug('Message API response: %s', rep)
                    return rep
                else:
                    logger.warning('Message API response: %s', rep)
                    raise SlackAPIError(rep)
            elif 300 <= response.status < 400:
                e = 'Redirection, status code: {}'.format(response.status)
                logger.error(e)
                raise SlackRedirectionError(e)
            elif 400 <= response.status < 500:
                e = 'Client error, status code: {}'.format(response.status)
                logger.error(e)
                raise SlackConnectionError(e)
            elif 500 <= response.status < 600:
                e = 'Server error, status code: {}'.format(response.status)
                raise SlackServerError(e)


class HTTPClient(_APICaller):
    """
    Client for the slack HTTP API.

    :param token: Slack API access token
    :param loop: Event loop, optional
    """

    async def delete(self, message: Message):
        """
        Delete a previously sent message

        :param message: Message previously sent
        :type message: Message
        :return: Timestamp of the message
        """
        logger.debug('Message Delete: %s', message)
        msg = self._prepare_message(message)
        rep = await self._do_post(_APIPath.DELETE_MSG, msg=msg)
        return rep.get('ts')

    async def send(self, message: Message):
        """
        Send a new message

        :param message: Message to send
        :type message: Message
        :return: Timestamp of the message
        """
        logger.debug('Message Sent: %s', message)
        msg = self._prepare_message(message)
        rep = await self._do_post(_APIPath.POST_MSG, msg=msg)
        return rep.get('ts')

    async def update(self, message: Message, timestamp: str=None):
        """
        Update a previously sent message

        If no timestamp if provided we assumed the timestamp of the previous
        message is stored in the new message. This enable the update of a
        message without creating a new message.

        :param message: New message
        :param timestamp: Timestamp of the message to update
        :return: Timestamp of the message
        """
        logger.debug('Message Update: %s', message)
        msg = self._prepare_message(message, timestamp)
        rep = await self._do_post(_APIPath.UPDATE_MSG, msg=msg)
        return rep.get('ts')

    def _prepare_message(self, message: Message, timestamp: str=None):
        """
        Format the message for the Slack API

        :param message: Message to send/update/delete
        :param timestamp: Timestamp of the message
        :return: Formatted msg
        :rtype: dict
        """
        msg = message.serialize()
        if timestamp:
            msg['ts'] = timestamp

        return msg

    async def add_reaction(self, message: Message, reaction: str='thumbsup'):
        """
        Add a reaction to a message

        See Slack API documentation and team settings for available reaction

        :param message: Message to add reaction to
        :param reaction: Reaction to add
        """
        msg = self._prepare_reaction(message, reaction)
        logger.debug('Reaction Add: %s', msg)
        await self._do_post(_APIPath.ADD_REACT, msg=msg)

    async def delete_reaction(self, message: Message, reaction: str):
        """
        Delete a reaction from a message

        :param message: Message to delete reaction from
        :param reaction: Reaction to delete
        """
        msg = self._prepare_reaction(message, reaction)
        logger.debug('Reaction Delete: %s', msg)
        await self._do_post(_APIPath.DELETE_REACT, msg=msg)

    async def get_reaction(self, message: Message):
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
        rep = await self._do_post(_APIPath.GET_REACT, msg=msg)
        return rep.get('message').get('reactions')

    def _prepare_reaction(self, message: Message, reaction: str=''):
        """
        Format the message and reaction for the Slack API

        :param message: Message to add/delete/get reaction
        :param reaction: Reaction to add/delete
        :return: Formatted message
        :rtype: dict
        """
        msg = message.serialize()
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
        logger.debug('Getting channels')
        all_channels = []
        bot_channels = []

        rep = await self._do_post(_APIPath.GET_CHANNEL, msg={})
        for chan in rep.get('channels'):
            channel = Channel(channel_id=chan['id'], **chan)
            all_channels.append(channel)
            if chan.get('is_member'):
                bot_channels.append(channel)

        return bot_channels, all_channels

    async def get_channels_info(self, channel_id: str):
        """
        Query the information about a channel

        :param channel_id: id of the channel to query
        :return: information
        :rtype: dict
        """
        msg = {
            'channel': channel_id
        }

        rep = await self._do_post(_APIPath.GET_CHANNEL_INFO, msg=msg)
        return rep['channel']


class RTMClient(_APICaller):
    """
    Client for the slack RTM API (websocket based API).

    :param token: Slack API Token
    :param loop: Event loop to work in, optional.
    """
    def __init__(self, token: str, *,
                 loop: Optional[asyncio.BaseEventLoop]=None):
        super().__init__(token, loop=loop)

        self._ws = None
        self._session = aiohttp.ClientSession()
        self._login_data = None
        self._closed = asyncio.Event(loop=self._loop)
        self._closed.set()

    @property
    def slack_id(self):
        if self._login_data is None:
            return None
        return self._login_data['self']['id']

    @property
    def is_closed(self) -> bool:
        """bool: Indicates if the websocket connection is closed."""
        return self._closed.is_set()

    async def _negotiate_rtm_url(self):
        """
        Get the RTM url
        """
        self._login_data = await self._do_post(_APIPath.RTM_START)

        if self._login_data.get('ok') is False:
            raise SlackConnectionError(
                'Error with slack {}'.format(self._login_data))

        # TODO: We will want to make sure to add in re-connection
        #       functionality if there is an error.
        return self._login_data['url']

    async def connect(self, queue: asyncio.Queue):
        """
        Connect to the websocket stream and iterate over the messages
        dumping them in the Queue.
        """
        ws_url = await self._negotiate_rtm_url()
        try:
            # TODO: We will need to put in some logic for re-connection
            #       on error.
            async with self._session.ws_connect(ws_url) as ws:
                self._closed.clear()
                self._ws = ws
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await queue.put(json.loads(msg.data))
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        logger.info('Slack websocket closed by remote.')
                        break  # noqa
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error('Websocket closed with error: %s.',
                                     ws.exception())
                        break  # noqa
        except asyncio.CancelledError:
            pass
        finally:
            self._closed.set()
            self._ws = None

    # Currently unused, only commenting out for the short term while
    # we work on some milestones for testing and cleanup
    # async def send_message(self, message, method='send', *args, **kwargs):
    #     if method == 'update':
    #         raise ValueError('RTMClient does not support message update.')

    #     data = {
    #         'type': 'message',
    #         'channel': message.to.id,
    #         'text': message.text
    #     }
    #     logger.debug('Message Sent: {}'.format(message))
    #     await self._ws.send(json.dumps(data))


class ClientFacade:
    """
    A class to compose all available functionality available to a bot
    or other plugin. This determines the appropriate channel to communicate
    with slack over (RTM or HTTP)
    """
    __slots__ = ('_http_client',)

    def __init__(self, http_client):
        self._http_client = http_client

    async def send(self, *messages):
        """
        Send the messages provided and update their timestamp

        :param messages: Messages to send
        """
        for message in messages:
            message.timestamp = await self._http_client.send(
                message=message)

    async def update(self, *messages):
        """
        Update the messages provided and update their timestamp

        :param messages: Messages to update
        """
        for message in messages:
            message.timestamp = await self._http_client.update(
                message=message)

    async def delete(self, *messages):
        """
        Delete the messages provided

        :param messages: Messages to delete
        """
        for message in messages:
            message.timestamp = await self._http_client.delete(message)

    async def add_reaction(self, *messages):
        """
        Add a reaction to a message

        :Example:

        >>> bot.add_reaction([Message, 'thumbsup'], [Message, 'robotface'])
        Add the thumbup and robotface reaction to the message

        :param messages: List of message and reaction to add
        """
        for message, reaction in messages:
            await self._http_client.add_reaction(message, reaction)

    async def delete_reaction(self, *messages):
        """
        Delete reactions from messages

        :Example:

        >>> bot.delete_reaction([Message, 'thumbsup'], [Message, 'robotface'])
        Delete the thumbup and robotface reaction from the message

        :param messages: List of message and reaction to delete
        """
        for message, reaction in messages:
            await self._http_client.delete_reaction(message, reaction)

    async def get_reactions(self, *messages):
        """
        Query the reactions of messages

        :param messages: Messages to query reaction from
        :return: dictionary of reactions by message
        :rtype: dict
        """
        reactions = dict()
        for message in messages:
            msg_reactions = await self._http_client.get_reaction(message)
            for msg_reaction in msg_reactions:
                users = list()
                for user_id in msg_reaction.get('users'):
                    users.append(User(user_id=user_id))
                msg_reaction['users'] = users
            reactions[message] = msg_reactions
            message.reactions = msg_reactions
        return reactions

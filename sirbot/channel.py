class ChannelManager:
    """
    Manager for the channel object.
    """
    def __init__(self, client):
        self._client = client
        self.channels = dict()
        self.names = dict()

    def add(self, *channels):
        """
        Add channels to the ChannelManager

        :param channels: id of the channel
        """
        for channel in channels:
            self.channels[channel.id] = channel
            self.names[channel.name] = channel.id

    def delete(self, *channels_id):
        """
        Delete channels from the ChannelManager

        :param channels_id: id of the channel
        """
        for channel_id in channels_id:
            name_del = False
            if channel_id in self.channels:
                del self.channels[channel_id]
            for name, id_ in self.names.items():
                if id_ == channel_id:
                    name_del = name
            if name_del:
                del self.names[name_del]

    async def get(self, _id=None, name=None, update=False):
        """
        Retrieve a channel from the ChannelManager.

        The name and the id are always available. To reliably have more
        information you should provide the complete argument to query the
        Slack API

        :param _id: id of the channel
        :param name: name of the channel
        :param update: Call Slack API to update the information about a channel
        :return: Channel
        """
        if name:
            _id = self.names.get(name)
        channel = self.channels.get(_id)

        if channel is not None and update:
            await self.update(channel)

        return channel

    async def update(self, channel):
        """
        Get a channel information

        :param channel: channel
        :return: channel
        """
        information = await self._client.get_channels_info(channel.id)
        channel.add(**information)
        return channel

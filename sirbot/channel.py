class ChannelManager:
    """
    Manager for the channel object.
    """
    def __init__(self):
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

    def get(self, _id=None, name=None):
        """
        Retrieve a channel from the ChannelManager

        :param _id: id of the channel
        :param name: name of the channel
        :return: Channel
        """
        if name:
            _id = self.names.get(name)
        return self.channels.get(_id)

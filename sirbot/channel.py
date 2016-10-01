class Channels:
    def __init__(self):
        self.channels = dict()
        self.names = dict()

    def add(self, *channels):
        for channel in channels:
            self.channels[channel.id] = channel
            self.names[channel.name] = channel.id

    def delete(self, *channels_id):
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
        if name:
            _id = self.names.get(name)
        return self.channels.get(_id)

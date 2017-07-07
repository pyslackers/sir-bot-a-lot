import logging

from collections import MutableMapping

from .errors import FrozenRegistryError

logger = logging.getLogger(__name__)


class Registry(MutableMapping):
    """
    Class regrouping all available plugin factory.

    The plugin factory is called each time the registry is queried.
    It is good practice to keep interacting on the same factory result without
    querying the registry each time.

    Similar behaviour as a dictionary
    """
    def __init__(self):
        super().__init__()
        self._frozen = False
        self._plugins = dict()

    @property
    def frozen(self):
        return self._frozen

    @frozen.setter
    def frozen(self, _):
        raise ValueError('Read only property')

    def freeze(self):
        self._frozen = True

    def __getitem__(self, item):
        return self._plugins[item]()

    def __setitem__(self, key, value):
        if not self._frozen:
            self._plugins[key] = value
        else:
            raise FrozenRegistryError()

    def __delitem__(self, key):
        raise FrozenRegistryError()

    def __iter__(self):
        return iter(self._plugins)

    def __len__(self):
        return len(self._plugins)

    def __contains__(self, item):
        return item in self._plugins

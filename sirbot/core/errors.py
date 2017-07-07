class SirBotError(Exception):
    """
    Top level sirbot error
    """


class RegistryError(SirBotError):
    """
    Class to compose all registry related errors
    """


class FrozenRegistryError(RegistryError):
    """
    Registry if frozen
    """

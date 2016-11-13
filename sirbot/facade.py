from sirbot.base import User


class BotFacade:
    """
    A class to compose all available functionality available to a bot
    or other plugin. This determines the appropriate channel to communicate
    with slack over (RTM or HTTP)
    """

    def __init__(self, http_client, scheduler):
        self._http_client = http_client
        self._scheduler = scheduler

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

        >>> chat.add_reaction([Message, 'thumbsup'], [Message, 'robotface'])
        Add the thumbup and robotface reaction to the message

        :param messages: List of message and reaction to add
        """
        for message, reaction in messages:
            await self._http_client.add_reaction(message, reaction)

    async def delete_reaction(self, *messages):
        """
        Delete reactions from messages

        :Example:

        >>> chat.delete_reaction([Message, 'thumbsup'], [Message, 'robotface'])
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

    def schedule(self, function, id_, trigger, *args, func_args=None,
                 func_kwargs=None, **kwargs):
        """
        Schedule a job

        :param function: function to be scheduled
        :param id_: id of the job
        :param trigger: trigger of the job
        :param func_args: list of args for the function
        :param func_kwargs: dict of kwargs for the function
        :return: Job
        """

        return self._scheduler.add_job(function, trigger, *args, id=id_,
                                       args=func_args, kwargs=func_kwargs,
                                       **kwargs)

    def unschedule(self, id_):
        """
        Unschedule a job based on his id

        :param id_: id of the job
        """
        if id_ not in []:  # To make sure nobody unschedule core jobs
            self._scheduler.remove_job(id_)

    def is_scheduled(self, id_):
        """
        Check if a given job is already scheduled

        :param id_: id of the job
        :return: Bool of job existence
        """
        rep = self._scheduler.get_job(id_)
        if rep is None:
            return False
        else:
            return True

import time
import logging

from sirbot.base import User

logger = logging.getLogger('sirbot')


class UserManager:
    """
    Manager for the user object
    """

    def __init__(self, client, scheduler):
        self._client = client
        self.users = dict()
        scheduler.add_job(self.clean_up, 'interval', id='UserManager',
                          minutes=10)

    def add(self, *users):
        """
        Add an user to the UserManager

        :param users: users to add
        """
        for user in users:
            self.users[user.id] = user

    async def get(self, id_=None, dm=False):
        """
        Return an User from the User Manager

        If the user doesn't exist query the slack API for it

        :param id_: id of the user
        :param dm: Query the direct message channel id
        :return: User
        """
        if id_.startswith('U'):
            # Filter only for actual user. Need implementation for bot user
            #  with the 'bots.info' API if we want bots talking to each other
            user = self.users.get(id_)

            if user is None:
                user = await self._client.get_user_info(id_)
                user = User(user['id'], **user)
                self.add(user)
            else:
                user.last_seen = time.time()

            if dm and user.send_id is None:
                dm_id = await self._client.get_user_dm_channel(id_)
                user.send_id = dm_id

            return user

    def clean_up(self):
        """
        Delete users not seen in 10 minutes from the users dict

        """
        last_seen_time = time.time() - 600
        to_delete = [id_ for id_, user in self.users.items()
                     if user.last_seen < last_seen_time]

        logger.debug('Cleaning user manager. Deleting: {}'.format(to_delete))

        for id_ in to_delete:
            self.users.pop(id_)

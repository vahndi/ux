from typing import List

from ux.interfaces.i_user import IUser


class User(IUser):
    """
    Represents a User.
    """
    def __init__(self, user_id: str, session_ids: list = None, action_ids: list = None):
        """
        Create a new User.
        :param user_id: The User's id.
        :param session_ids: A list of id's of Sessions that the User took Actions in.
        :param action_ids: A list of the id's of Actions that the User took.
        """
        self._user_id = user_id
        self._session_ids = session_ids or []
        self._action_ids = action_ids or []

    @property
    def user_id(self):
        """
        Return the User's id

        :rtype: str
        """
        return self._user_id

    @property
    def action_ids(self):
        """
        Return the list of id's of the Actions the User took.

        :rtype: List[str]
        """
        return self._action_ids

    @property
    def session_ids(self):
        """
        Return the list of id's of the Sessions the User took Actions in.

        :rtype: List[str]
        """
        return self._session_ids

    def add_action_id(self, action_id: str):
        """
        Add an Action id to the list of the User's Actions.

        :param action_id: The id of the Action to add.
        """
        self._action_ids.append(action_id)

    def add_session_id(self, session_id: str):
        """
        Add a Session id to the list of the User's Sessions.

        :param session_id: The id of the Action to add.
        """
        self._session_ids.append(session_id)

    def __repr__(self):

        return 'User({})'.format(self._user_id)

from typing import List, Optional


class User(object):
    """
    Represents a User.
    """
    def __init__(self, user_id: str, session_ids: Optional[List[str]] = None, action_ids: Optional[List[str]] = None):
        """
        Create a new User.
        :param user_id: The User's id.
        :param session_ids: A list of id's of Sessions that the User took Actions in.
        :param action_ids: A list of the id's of Actions that the User took.
        """
        self._user_id: str = user_id
        self._session_ids: List[str] = session_ids or []
        self._action_ids: List[str] = action_ids or []

    @property
    def user_id(self) -> str:
        """
        Return the User's id
        """
        return self._user_id

    @property
    def action_ids(self) -> List[str]:
        """
        Return the list of id's of the Actions the User took.
        """
        return self._action_ids

    @property
    def session_ids(self) -> List[str]:
        """
        Return the list of id's of the Sessions the User took Actions in.
        """
        return self._session_ids

    def add_action_id(self, action_id: str) -> None:
        """
        Add an Action id to the list of the User's Actions.

        :param action_id: The id of the Action to add.
        """
        self._action_ids.append(action_id)

    def add_session_id(self, session_id: str) -> None:
        """
        Add a Session id to the list of the User's Sessions.

        :param session_id: The id of the Action to add.
        """
        self._session_ids.append(session_id)

    def __repr__(self) -> str:

        return 'User({})'.format(self._user_id)

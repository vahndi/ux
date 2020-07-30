from datetime import datetime
from typing import Optional, Callable, Union, List, Any

from ux.actions.action_template import ActionTemplate


class UserAction(object):
    """
    Represents an Action taken by a User.
    """
    def __init__(self, action_id: str, action_type: str, source_id: str,
                 time_stamp: datetime, user_id: str, session_id: str,
                 target_id: str = None, meta: dict = None):
        """
        Create a new UserAction.

        :param action_id: The id of the Action taken.
        :param action_type: The type of Action taken.
        :param source_id: The id of the location where the User took the Action.
        :param time_stamp: The date-time when the User took the Action.
        :param user_id: The id of the User who took the Action.
        :param session_id: The id of the Session in which the User took the
                           Action.
        :param target_id: Optional id of the location the Action navigated to.
        :param meta: Optional additional data to store with the UserAction.
        """
        self._action_type: str = action_type
        self._source_id: str = source_id
        self._target_id: str = target_id
        self._action_id: str = action_id
        self._time_stamp: datetime = time_stamp
        self._user_id: str = user_id
        self._session_id: str = session_id
        self._meta: dict = meta
        self._action_template: Optional[ActionTemplate] = None

    @property
    def action_type(self) -> str:
        """
        Return the type of Action taken.
        """
        return self._action_type

    @property
    def source_id(self) -> str:
        """
        Return the id of the location where the User took the Action.
        """
        return self._source_id

    @property
    def target_id(self) -> str:
        """
        Return the id of the location where the Action took the User to.
        """
        return self._target_id

    @property
    def action_id(self) -> str:
        """
        Return the id of the Action taken.
        """
        return self._action_id

    @property
    def time_stamp(self) -> datetime:
        """
        Return the date-time the Action was taken.
        """
        return self._time_stamp

    @property
    def user_id(self) -> str:
        """
        Return the id of the User who took the Action.
        """
        return self._user_id

    @property
    def session_id(self) -> str:
        """
        Return the id of the Session in which the User took the Action.
        """
        return self._session_id

    @property
    def meta(self) -> dict:
        """
        Return any additional data stored with the UserAction.
        """
        return self._meta

    def template(self) -> ActionTemplate:
        """
        Return an ActionTemplate that corresponds to the Action.
        """
        if self._action_template is None:
            self._action_template = ActionTemplate(
                action_type=self._action_type,
                source_id=self._source_id,
                target_id=self._target_id
            )
        return self._action_template

    def __repr__(self) -> str:

        return 'UserAction({}: {}{}{})'.format(
            self._action_type, self._source_id,
            ' -> ' if self._target_id else '',
            self._target_id if self._target_id else ''
        )


ActionCounter = Callable[[UserAction], Union[str, List[str]]]
ActionFilter = Callable[[UserAction], bool]
ActionMapper = Callable[[UserAction], Any]
ActionGrouper = Callable[[UserAction], Any]

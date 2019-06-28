from datetime import datetime
from typing import Iterable

from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.classes.actions.action_template import ActionTemplate


class UserAction(IUserAction):
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
        :param session_id: The id of the Session in which the User took the Action.
        :param target_id: Optional id of the location the Action navigated to.
        :param meta: Optional additional data to store with the UserAction.
        """
        self._action_type = action_type
        self._source_id = source_id
        self._target_id = target_id
        self._action_id = action_id
        self._time_stamp = time_stamp
        self._user_id = user_id
        self._session_id = session_id
        self._meta = meta

    @property
    def action_type(self):
        """
        Return the type of Action taken.

        :rtype: str
        """
        return self._action_type

    @property
    def source_id(self):
        """
        Return the id of the location where the User took the Action.

        :rtype: str
        """
        return self._source_id

    @property
    def target_id(self):
        """
        Return the id of the location where the Action took the User to.

        :rtype: str
        """
        return self._target_id

    @property
    def action_id(self):
        """
        Return the id of the Action taken.

        :rtype: str
        """
        return self._action_id

    @property
    def time_stamp(self):
        """
        Return the date-time the Action was taken.

        :rtype: datetime
        """
        return self._time_stamp

    @property
    def user_id(self):
        """
        Return the id of the User who took the Action.

        :rtype: str
        """
        return self._user_id

    @property
    def session_id(self):
        """
        Return the id of the Session in which the User took the Action.

        :rtype: str
        """
        return self._session_id

    @property
    def meta(self):
        """
        Return any additional data stored with the UserAction.

        :rtype: dict
        """
        return self._meta

    def template(self):
        """
        Return an ActionTemplate that corresponds to the Action.

        :rtype: IActionTemplate
        """
        return ActionTemplate(
            action_type=self._action_type,
            source_id=self._source_id,
            target_id=self._target_id
        )

    @staticmethod
    def templates(user_actions):
        """
        Return a list of ActionTemplates corresponding to the given list of Actions.

        :type user_actions: Iterable[UserAction]
        :rtype: List[ActionTemplate]
        """
        return [
            user_action.template()
            for user_action in user_actions
        ]

    def __repr__(self):

        return 'UserAction({}: {}{}{})'.format(
            self._action_type, self._source_id,
            ' -> ' if self._target_id else '',
            self._target_id if self._target_id else ''
        )

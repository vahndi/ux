from datetime import datetime
from typing import Iterable

from ux.classes.ux.action_template import ActionTemplate
from ux.interfaces.ux.i_user_action import IUserAction


class UserAction(IUserAction):

    def __init__(self, action_id: str, action_type: str, source_id: str,
                 time_stamp: datetime, user_id: str, session_id: str,
                 target_id: str = None, extra: dict = None):

        self._action_type = action_type
        self._source_id = source_id
        self._target_id = target_id
        self._action_id = action_id
        self._time_stamp = time_stamp
        self._user_id = user_id
        self._session_id = session_id
        self._extra = extra

    @property
    def action_type(self):
        return self._action_type

    @property
    def source_id(self):
        return self._source_id

    @property
    def target_id(self):
        return self._target_id

    @property
    def action_id(self):
        return self._action_id

    @property
    def time_stamp(self):
        return self._time_stamp

    @property
    def user_id(self):
        return self._user_id

    @property
    def session_id(self):
        return self._session_id

    @property
    def extra(self):
        return self._extra

    def template(self):
        """
        :rtype: ActionTemplate
        """
        return ActionTemplate(
            action_type=self._action_type,
            source_id=self._source_id,
            target_id=self._target_id
        )

    @staticmethod
    def templates(user_actions):
        """
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
            '->' if self._target_id else '',
            self._target_id if self._target_id else ''
        )

from typing import Iterable

from ux.interfaces.actions.i_action_template import IActionTemplate


class IUserAction(object):

    @property
    def action_type(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def source_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def target_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def action_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def time_stamp(self):
        """
        :rtype: datetime
        """
        raise NotImplementedError

    @property
    def user_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def session_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def meta(self):
        """
        :rtype: dict
        """
        raise NotImplementedError

    def template(self):
        """
        :rtype: IActionTemplate
        """
        raise NotImplementedError

    @staticmethod
    def templates(user_actions):
        """
        :type user_actions: Iterable[IUserAction]
        :rtype: Iterable[IActionTemplate]
        """
        raise NotImplementedError

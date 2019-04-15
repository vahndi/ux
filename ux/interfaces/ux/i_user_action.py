from typing import Iterable

from ux.interfaces.ux.i_action_template import IActionTemplate


class IUserAction(object):

    @property
    def action_type(self):
        raise NotImplementedError

    @property
    def source_id(self):
        raise NotImplementedError

    @property
    def target_id(self):
        raise NotImplementedError

    @property
    def action_id(self):
        raise NotImplementedError

    @property
    def time_stamp(self):
        raise NotImplementedError

    @property
    def user_id(self):
        raise NotImplementedError

    @property
    def session_id(self):
        raise NotImplementedError

    @property
    def extra(self):
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

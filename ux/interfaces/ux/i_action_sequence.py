from typing import List

from ux.interfaces.ux.i_user_action import IUserAction


class IActionSequence(object):

    @property
    def user_actions(self):
        """
        :rtype: List[IUserAction]
        """
        raise NotImplementedError

    def action_templates(self):

        raise NotImplementedError

    @property
    def extra(self):
        """
        :rtype: dict
        """
        raise NotImplementedError

    def duration(self):

        raise NotImplementedError

    def unordered_completion_rate(self, task):

        raise NotImplementedError

    def ordered_completion_rate(self, task):

        raise NotImplementedError

    def intersects_task(self, task):

        raise NotImplementedError

    def __len__(self):
        """
        should return the  number of user actions
        """
        raise NotImplementedError

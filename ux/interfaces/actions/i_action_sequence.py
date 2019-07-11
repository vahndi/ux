from typing import List, Set

from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.i_location import ILocation


class IActionSequence(object):

    @property
    def user_actions(self):
        """
        :rtype: List[IUserAction]
        """
        raise NotImplementedError

    def action_templates(self):
        """
        :rtype: List[IActionTemplate]
        """
        raise NotImplementedError

    @property
    def meta(self):
        """
        :rtype: dict
        """
        raise NotImplementedError

    def duration(self):
        """
        :rtype: timedelta
        """
        raise NotImplementedError

    def unordered_completion_rate(self, task):
        """
        :type task: ITask
        :rtype: float
        """
        raise NotImplementedError

    def ordered_completion_rate(self, task):
        """
        :type task: ITask
        :rtype: float
        """
        raise NotImplementedError

    def intersects_task(self, task):
        """
        :type task: ITask
        :rtype: bool
        """
        raise NotImplementedError

    def location_ids(self):
        """
        :rtype: Set[str]
        """
        raise NotImplementedError

    def contains_action_template(self, action_template):
        """
        Returns True if the sequence contains a User Action which matches the given Template.

        :param action_template: The ActionTemplate to match against.
        :type action_template: IActionTemplate
        :rtype: bool
        """
        raise NotImplementedError

    def __len__(self):
        """
        should return the  number of user actions
        """
        raise NotImplementedError

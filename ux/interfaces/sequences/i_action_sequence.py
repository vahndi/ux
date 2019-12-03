from typing import List, Set

from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.actions.i_user_action import IUserAction


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

    def action_template_set(self):
        """
        Return a set of ActionTemplates representing the UserActions in the ActionSequence.

        :rtype: Set[IActionTemplate]
        """
        raise NotImplementedError

    def action_template_counts(self, rtype: type = dict):
        """
        Return a count of each ActionTemplate representing one or more UserActions in the ActionSequence.

        :rtype: Dict[IActionTemplate, int]
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

    def start_date_time(self):
        """
        :rtype: datetime
        """
        raise NotImplementedError

    def end_date_time(self):
        """
        :rtype: datetime
        """
        raise NotImplementedError

    def map(self, mapper, rtype: type = dict):
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

    def action_types(self):
        """
        :rtype: Set[str]
        """
        raise NotImplementedError

    def location_ids(self):
        """
        :rtype: Set[str]
        """
        raise NotImplementedError

    def contains_location_id(self, location_id: str):
        """
        Determine whether the location was visited in the sequence.

        :rtype: bool
        """
        raise NotImplementedError

    def find_all(self, template: IActionTemplate):
        """
        Return a list of all the actions matching the given action template.
        Returns an empty list if the template is not matched.

        :param template: The ActionTemplate to match against.
        :rtype: list[IUserAction]
        """
        raise NotImplementedError

    def find_first(self, template: IActionTemplate):
        """
        Return the first action matching the given action template. Returns None if the template is not matched.

        :param template: The ActionTemplate to match against.
        :rtype: IUserAction
        """
        raise NotImplementedError

    def find_last(self, template: IActionTemplate):
        """
        Return the first action matching the given action template. Returns None if the template is not matched.

        :param template: The ActionTemplate to match against.
        :rtype: IUserAction
        """
        raise NotImplementedError

    def __getitem__(self, item):
        """
        :rtype: IUserAction
        """
        raise NotImplementedError

    def __len__(self):
        """
        :rtype: int
        """
        raise NotImplementedError

    def __contains__(self, item):
        """
        :rtype: bool
        """
        raise NotImplementedError

    def __iter__(self):
        """
        :rtype: IUserAction
        """
        raise NotImplementedError

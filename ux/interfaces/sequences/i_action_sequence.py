from collections import Counter
from datetime import timedelta, datetime
from typing import List, Set, Iterator, Dict, Union

from ux.classes.wrappers.map_result import MapResult
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.tasks.i_task import ITask


class IActionSequence(object):

    @property
    def user_actions(self) -> List[IUserAction]:

        raise NotImplementedError

    @property
    def meta(self) -> dict:

        raise NotImplementedError

    @property
    def duration(self) -> timedelta:

        raise NotImplementedError

    @property
    def start(self) -> datetime:

        raise NotImplementedError

    @property
    def end(self) -> datetime:

        raise NotImplementedError

    @property
    def user_id(self) -> str:

        raise NotImplementedError

    @property
    def session_id(self) -> str:

        raise NotImplementedError

    def action_templates(self) -> List[IActionTemplate]:

        raise NotImplementedError

    def action_template_set(self) -> Set[IActionTemplate]:

        raise NotImplementedError

    def action_template_counts(self) -> Dict[IActionTemplate, int]:
        """
        Return a count of each ActionTemplate representing one or more UserActions in the ActionSequence.
        """
        raise NotImplementedError

    def map(self, mapper) -> MapResult:

        raise NotImplementedError

    def unordered_completion_rate(self, task: ITask) -> float:

        raise NotImplementedError

    def ordered_completion_rate(self, task: ITask) -> float:

        raise NotImplementedError

    def intersects_task(self, task: ITask) -> bool:

        raise NotImplementedError

    def action_types(self) -> Set[str]:

        raise NotImplementedError

    def back_click_rates(self) -> Dict[IActionTemplate, float]:

        raise NotImplementedError

    def filter(self, condition, copy_meta: bool = False):
        """
        :rtype: IActionSequence
        """
        raise NotImplementedError

    def count(self, condition) -> int:
        """
        Return a count of the UserActions where the given condition is True
        """
        raise NotImplementedError

    def counter(self, get_value) -> Counter:
        """
        Return a dict of counts for each value returned by get_value(action) for each action.

        :param get_value: method that returns a str or list of strs when called on an action.
        """
        raise NotImplementedError

    def dwell_times(self, sum_by_location: bool) -> Dict[str, Union[timedelta, List[timedelta]]]:
        """
        Return the amount of time spent by the user at each location.

        :param sum_by_location: Whether to sum the durations of time spent at each location or keep as a list.
        """
        raise NotImplementedError

    def location_ids(self) -> Set[str]:

        raise NotImplementedError

    def contains_location_id(self, location_id: str) -> bool:
        """
        Determine whether the location was visited in the sequence.
        """
        raise NotImplementedError

    def find_all(self, template: IActionTemplate) -> List[IUserAction]:
        """
        Return a list of all the actions matching the given action template.
        Returns an empty list if the template is not matched.

        :param template: The ActionTemplate to match against.
        """
        raise NotImplementedError

    def find_first(self, template: IActionTemplate) -> IUserAction:
        """
        Return the first action matching the given action template. Returns None if the template is not matched.

        :param template: The ActionTemplate to match against.
        """
        raise NotImplementedError

    def find_last(self, template: IActionTemplate) -> IUserAction:
        """
        Return the first action matching the given action template. Returns None if the template is not matched.

        :param template: The ActionTemplate to match against.
        """
        raise NotImplementedError

    def __getitem__(self, item) -> IUserAction:

        raise NotImplementedError

    def __len__(self) -> int:

        raise NotImplementedError

    def __contains__(self, item) -> bool:

        raise NotImplementedError

    def __iter__(self) -> Iterator[IUserAction]:

        raise NotImplementedError

from collections import defaultdict
from datetime import datetime, timedelta
from types import FunctionType
from typing import List, Callable, Any, Set

from pandas import Series, DataFrame

from ux.calcs.object_calcs.efficiency import lostness
from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate, \
    binary_task_success
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.tasks.i_task import ITask
from ux.interfaces.actions.i_user_action import IUserAction
from ux.utils.actions import create_action_template_condition
from ux.utils.misc import get_method_name


class ActionSequence(IActionSequence):
    """
    Represents a sequence of UserActions taken by a User.
    """

    def __init__(self, user_actions: List[IUserAction] = None, meta: dict = None):
        """
        Create a new ActionSequence.

        :param user_actions: List of Actions to use to construct the ActionSequence.
        :param meta: Optional additional data to store with the ActionSequence.
        """
        self._user_actions = user_actions or []
        self._meta = meta
        self._action_templates = None
        self._location_ids = None

    @property
    def user_actions(self):
        """
        Return the list of UserActions in the ActionSequence.

        :rtype: List[IUserAction]
        """
        return self._user_actions

    @property
    def meta(self):
        """
        Return the dictionary of meta information added at construction time.

        :rtype: dict
        """
        return self._meta

    def action_templates(self):
        """
        Return a list of ActionTemplates derived from each of the UserActions taken.

        :rtype: List[IActionTemplate]
        """
        if self._action_templates is None:
            self._action_templates = [
                user_action.template()
                for user_action in self._user_actions
            ]
        return self._action_templates

    def action_template_set(self):
        """
        Return a set of ActionTemplates representing the UserActions in the ActionSequence.

        :rtype: Set[IActionTemplate]
        """
        return set(self.action_templates())

    def action_template_counts(self, rtype: type = dict):
        """
        Return a count of each ActionTemplate representing one or more UserActions in the ActionSequence.

        :rtype: Dict[IActionTemplate, int]
        """
        counts = defaultdict(int)
        for template in self.action_templates():
            counts[template] += 1
        if rtype is dict:
            return dict(counts)
        elif rtype is Series:
            return Series(counts).sort_values(ascending=False)
        else:
            raise TypeError('rtype must be dict or Series')

    def contains_action_template(self, action_template):
        """
        Returns True if the sequence contains a User Action which matches the given Template.

        :param action_template: The ActionTemplate to match against.
        :type action_template: IActionTemplate
        :rtype: bool
        """
        return action_template in self.action_templates()

    def first_action_occurrence(self, action_template):
        """
        Return the first action matching the given action template. Returns None if the template is not matched.

        :type action_template: IActionTemplate
        :rtype: IUserAction
        """
        occurrences = self.all_action_occurrences(action_template)
        if len(occurrences):
            return occurrences[0]
        else:
            return None

    def all_action_occurrences(self, action_template):
        """
        Return a list of all the actions matching the given action template.
        Returns an empty list if the template is not matched.

        :param action_template: The ActionTemplate to match against.
        :type action_template: IActionTemplate
        :rtype: list[IUserAction]
        """
        return [action for action in self.user_actions
                if action.template() == action_template]

    def start_date_time(self):
        """
        :rtype: datetime
        """
        return self._user_actions[0].time_stamp

    def end_date_time(self):
        """
        :rtype: datetime
        """
        return self._user_actions[-1].time_stamp

    def duration(self):
        """
        Return the total duration of the ActionSequence from the first Action to the last.

        :rtype: timedelta
        """
        start_time = self.user_actions[0].time_stamp
        end_time = self.user_actions[-1].time_stamp
        return end_time - start_time

    def map(self, mapper, rtype: type = dict):
        """
        Apply a map function to every action in the Sequence and return the results.

        :param mapper: The method or methods to apply to each UserAction
        :type mapper: Union[str, dict, Callable[[IUserAction], Any]]
        :param rtype: Return type of the result: dict or DataFrame
        """
        def map_items(item_mapper):
            if isinstance(item_mapper, str):
                if hasattr(IUserAction, item_mapper):
                    if callable(getattr(IUserAction, item_mapper)):
                        return [getattr(action, item_mapper)() for action in self._user_actions]
                    else:
                        return [getattr(action, item_mapper) for action in self._user_actions]
            elif isinstance(item_mapper, FunctionType):
                return [item_mapper(action) for action in self._user_actions]

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            results = {get_method_name(mapper): map_items(mapper)}
        elif isinstance(mapper, dict):
            results = {
                get_method_name(key): map_items(value)
                for key, value in mapper.items()
            }
        else:
            raise TypeError('mapper must be of type list, dict, str or function')
        if rtype is dict:
            return results
        elif rtype is DataFrame:
            return DataFrame(results)
        else:
            raise TypeError('rtype must be dict or DataFrame')

    def intersects_task(self, task: ITask):
        """
        Return True if the given Task has ActionTemplates that are equivalent to any Actions in the Sequence.

        :param task: Task to cross-reference Action Templates against.
        :rtype: bool
        """
        return sequence_intersects_task(action_sequence=self, task=task)

    def binary_task_success(self, task: ITask,
                            success_func: Callable[[ITask, IActionSequence], bool]):
        """
        Return True if success_func is met.

        :param task: The Task to assess success against.
        :param success_func: Callable to use to assess success.
        :rtype: bool
        """
        return binary_task_success(
            task=task, action_sequence=self,
            success_func=success_func
        )

    def lostness(self, task: ITask):
        """
        Return the lostness with respect to the given Task.

        :param task: The Task to calculate lostness against.
        :rtype: float
        """
        return lostness(task=task, action_sequence=self)

    def split(self, split, how: str = 'at', copy_meta: bool = False):
        """
        Split into a list of new ActionSequences after each `UserAction` where `condition` is met.

        :param split: Lambda function or Action Template to use to break the sequence.
        :type split: Union[ActionFilter, IActionTemplate]
        :param how: How to split the Sequence. One of `['before', 'after', 'at']`
        :param copy_meta: Whether to copy the `meta` dict into the new Sequences.
        :rtype: List[IActionSequence]
        """
        # find matching locations
        match_locs = []
        condition = create_action_template_condition(split)
        for a, action in enumerate(self.user_actions):
            if condition(action):
                match_locs.append(a)
        # split at right locations depending on the value of `how`
        if how == 'before':
            seq_starts = [m for m in match_locs]
            seq_ends = [m for m in match_locs if m != 0] + [len(self)]
            if match_locs[0] != 0:
                seq_starts.insert(0, 0)
            if match_locs[-1] == len(self):
                seq_ends = seq_ends[: -1]
        elif how == 'after':
            seq_starts = [0] + [m + 1 for m in match_locs]
            if seq_starts[-1] == len(self):
                seq_starts = seq_starts[: -1]
            seq_ends = [m + 1 for m in match_locs]
            if seq_ends[-1] != len(self):
                seq_ends.append(len(self))
        elif how == 'at':
            seq_starts = [m + 1 for m in match_locs if m != len(self) - 1]
            if match_locs[0] != 0:
                seq_starts.insert(0, 0)
            seq_ends = [m for m in match_locs if m != 0]
            if match_locs[-1] != len(self) - 1:
                seq_ends.append(len(self))
        else:
            raise ValueError("'how' must be set to one of ['before', 'after', 'at']")

        return [ActionSequence(
            user_actions=self.user_actions[start: end],
            meta=self._meta if copy_meta else None
        ) for start, end in zip(seq_starts, seq_ends)]

    def crop(self, start, end, how: str, copy_meta: bool = False):
        """
        Crop the sequence to start and end ActionTemplates or conditions.
        Returns None if both conditions are not found in order.

        :param start: The start of the subsequence to crop to.
        :param end: The end of the subsequence to crop to.
        :param how: 'first' or 'last'
        :param copy_meta: Whether to copy the `meta` dict into the new Sequence.
        :rtype: IActionSequence
        """
        start = create_action_template_condition(start)
        end = create_action_template_condition(end)
        a_start = None
        a_end = None
        if how == 'first':
            for a in range(len(self)):
                if start(self[a].template()):
                    a_start = a
                    break
            if a_start is not None and a_start < len(self) - 1:
                for a in range(a_start + 1, len(self)):
                    if end(self[a].template()):
                        a_end = a
                        break
        elif how == 'last':
            for a in range(len(self) - 1, -1, -1):
                if end(self[a].template()):
                    a_end = a
                    break
            if a_end is not None and a_end > 0:
                for a in range(a_end - 1, -1, -1):
                    if start(self[a].template()):
                        a_start = a
                        break
        else:
            raise ValueError("'how' must be one of 'first' or 'last'")
        if None in (a_start, a_end):
            return None
        else:
            return ActionSequence(
                user_actions=self.user_actions[a_start: a_end + 1],
                meta=self._meta if copy_meta else None
            )

    def unordered_completion_rate(self, task: ITask):
        """
        Calculate the unordered completion rate of the given Task from the Actions in the Sequence.

        :param task: The Task to cross-reference UserActions against.
        :rtype: float
        """
        return unordered_task_completion_rate(task, self)

    def ordered_completion_rate(self, task: ITask):
        """
        Calculate the ordered completion rate of the given Task from the Actions in the Sequence.

        :param task: The Task to cross-reference UserActions against.
        :rtype: float
        """
        return ordered_task_completion_rate(task, self)

    def location_ids(self):
        """
        Return a set of the ids of the unique locations visited in the sequence.

        :rtype: Set[str]
        """
        if self._location_ids is None:
            location_ids = set()
            for action in self._user_actions:
                location_ids.add(action.source_id)
                if action.target_id:
                    location_ids.add(action.target_id)
            self._location_ids = location_ids
        return self._location_ids

    def contains_location_id(self, location_id: str):
        """
        Determine whether the location was visited in the sequence.

        :rtype: bool
        """
        return location_id in self.location_ids()

    def action_types(self):
        """
        Return a set of the unique action types carried out in the sequence.

        :rtype: Set[str]
        """
        return set([action.action_type for action in self.user_actions])

    def __getitem__(self, item):
        """
        :rtype: IUserAction
        """
        return self._user_actions[item]

    def __repr__(self):
        """
        :rtype: str
        """
        return 'ActionSequence([{}])'.format(
            len(self._user_actions)
        )

    def __len__(self):
        """
        :rtype: int
        """
        return len(self._user_actions)

    def __contains__(self, item):
        """
        :rtype: bool
        """
        if isinstance(item, IUserAction):
            return item in self._user_actions
        elif isinstance(item, IActionTemplate):
            return item in self.action_templates()
        else:
            raise TypeError('item must be IUserAction or IActionTemplate')

    def __iter__(self):
        """
        :rtype: IUserAction
        """
        return self._user_actions.__iter__()

from collections import defaultdict, OrderedDict, Counter
from datetime import datetime, timedelta
from types import FunctionType
from typing import List, Callable, Set, Union, Iterator, Dict

from pandas import notnull

from ux.calcs.object_calcs.efficiency import lostness
from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate, \
    binary_task_success
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.classes.wrappers.map_result import MapResult
from ux.custom_types.action_types import ActionMapper, ActionFilter, ActionCounter
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.tasks.i_task import ITask
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
    def user_actions(self) -> List[IUserAction]:
        """
        Return the list of UserActions in the ActionSequence.
        """
        return self._user_actions

    @property
    def meta(self) -> dict:
        """
        Return the dictionary of meta information added at construction time.
        """
        return self._meta

    @property
    def start(self) -> datetime:

        return self[0].time_stamp

    @property
    def end(self) -> datetime:

        return self[-1].time_stamp

    @property
    def duration(self) -> timedelta:
        """
        Return the total duration of the ActionSequence from the first Action to the last.
        """
        start_time = self[0].time_stamp
        end_time = self[-1].time_stamp
        return end_time - start_time

    @property
    def user_id(self) -> str:

        return self[0].user_id

    @property
    def session_id(self) -> str:

        return self[0].session_id

    def action_templates(self) -> List[IActionTemplate]:
        """
        Return a list of ActionTemplates derived from each of the UserActions taken.
        """
        if self._action_templates is None:
            self._action_templates = [
                user_action.template()
                for user_action in self._user_actions
            ]
        return self._action_templates

    def action_template_set(self) -> Set[IActionTemplate]:
        """
        Return a set of ActionTemplates representing the UserActions in the ActionSequence.
        """
        return set(self.action_templates())

    def action_template_counts(self) -> Dict[IActionTemplate, int]:
        """
        Return a count of each ActionTemplate representing one or more UserActions in the ActionSequence.
        """
        counts = defaultdict(int)
        for template in self.action_templates():
            counts[template] += 1
        return dict(counts)

    def filter(self, condition: Union[ActionFilter, IActionTemplate], copy_meta: bool = False) -> IActionSequence:

        if condition in (None, True):
            return self
        if isinstance(condition, IActionTemplate):
            actions = self.find_all(condition)
        elif isinstance(condition, FunctionType):
            actions = [a for a in self if condition(a)]
        else:
            raise TypeError('filter condition must be ActionFilter or IActionTemplate')
        return ActionSequence(
            user_actions=actions,
            meta=self.meta if copy_meta else {}
        )

    def count(self, condition: Union[ActionFilter, IActionTemplate] = None) -> int:
        """
        Return a count of the UserActions where the given condition is True
        """
        if condition in (None, True):
            return len(self)
        action_count = 0
        if isinstance(condition, IActionTemplate):
            return len(self.find_all(condition))
        elif isinstance(condition, FunctionType):
            for action in self._user_actions:
                if condition(action):
                    action_count += 1
            return action_count
        else:
            raise TypeError('count condition must be ActionFilter or IActionTemplate')

    def counter(self, get_value: ActionCounter) -> Counter:
        """
        Return a dict of counts of each value returned by get_value(action) for each action.

        If get_value returns a list then 1 will be added to the counter value for each element key of the list.
        If get_value returns a non-list then the returned item will be used as a key and it's value increased by 1.

        :param get_value: method that returns a str or list of strs when called on an action.
        """
        counts = Counter()
        for action in self:
            action_result = get_value(action)
            if isinstance(action_result, list):
                counts += Counter(action_result)
            elif isinstance(action_result, str):
                counts[action_result] += 1
            else:
                raise TypeError('get_value must return str or list of str')
        return counts

    def find_all(self, template: IActionTemplate) -> List[IUserAction]:
        """
        Return a list of all the actions matching the given action template.
        Returns an empty list if the template is not matched.

        :param template: The ActionTemplate to match against.
        """
        return [action for action in self if action.template() == template]

    def find_first(self, template: IActionTemplate) -> IUserAction:
        """
        Return the first action matching the given action template. Returns None if the template is not matched.
        """
        occurrences = self.find_all(template)
        if len(occurrences):
            return occurrences[0]
        else:
            return None

    def find_last(self, template: IActionTemplate) -> IUserAction:
        """
        Return the first action matching the given action template. Returns None if the template is not matched.
        """
        occurrences = self.find_all(template)
        if len(occurrences):
            return occurrences[-1]
        else:
            return None

    def map(self, mapper: Union[str, dict, list, ActionMapper]) -> MapResult:
        """
        Apply a map function to every action in the Sequence and return the results.

        :param mapper: The method or methods to apply to each UserAction
        """
        def map_items(item_mapper):
            if isinstance(item_mapper, str):
                # properties and methods
                if hasattr(IUserAction, item_mapper):
                    if callable(getattr(IUserAction, item_mapper)):
                        # methods
                        return [getattr(action, item_mapper)() for action in self]
                    else:
                        # properties
                        return [getattr(action, item_mapper) for action in self]
            elif isinstance(item_mapper, FunctionType):
                return [item_mapper(action) for action in self._user_actions]
            else:
                raise TypeError('item mappers must be FunctionType or str')

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            results = OrderedDict([(get_method_name(mapper), map_items(mapper))])
        elif isinstance(mapper, dict):
            results = OrderedDict([
                (get_method_name(key), map_items(value))
                for key, value in mapper.items()
            ])
        elif isinstance(mapper, list):
            results = OrderedDict([
                (get_method_name(item), map_items(item))
                for item in mapper
            ])
        else:
            raise TypeError('mapper must be dict, str or FunctionType')

        return MapResult(results)

    def intersects_task(self, task: ITask) -> bool:
        """
        Return True if the given Task has ActionTemplates that are equivalent to any Actions in the Sequence.

        :param task: Task to cross-reference Action Templates against.
        """
        return sequence_intersects_task(action_sequence=self, task=task)

    def binary_task_success(self, task: ITask,
                            success_func: Callable[[ITask, IActionSequence], bool]) -> bool:
        """
        Return True if success_func is met.

        :param task: The Task to assess success against.
        :param success_func: Callable to use to assess success.
        """
        return binary_task_success(
            task=task, action_sequence=self,
            success_func=success_func
        )

    def lostness(self, task: ITask) -> float:
        """
        Return the lostness with respect to the given Task.

        :param task: The Task to calculate lostness against.
        """
        return lostness(task=task, action_sequence=self)

    def split(self, split, how: str = 'at', copy_meta: bool = False) -> List[IActionSequence]:
        """
        Split into a list of new ActionSequences after each `UserAction` where `condition` is met.

        :param split: Lambda function or Action Template to use to break the sequence.
        :type split: Union[ActionFilter, IActionTemplate]
        :param how: How to split the Sequence. One of `['before', 'after', 'at']`
        :param copy_meta: Whether to copy the `meta` dict into the new Sequences.
        """
        # find matching locations
        match_locs = []
        condition = _create_action_template_condition(split)
        for a, action in enumerate(self):
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
            user_actions=self[start: end],
            meta=self._meta if copy_meta else None
        ) for start, end in zip(seq_starts, seq_ends)]

    def crop(self, start, end, how: str, copy_meta: bool = False) -> IActionSequence:
        """
        Crop the sequence to start and end ActionTemplates or conditions.
        Returns None if both conditions are not found in order.

        :param start: The start of the subsequence to crop to.
        :param end: The end of the subsequence to crop to.
        :param how: 'first' or 'last'
        :param copy_meta: Whether to copy the `meta` dict into the new Sequence.
        """
        start = _create_action_template_condition(start)
        end = _create_action_template_condition(end)
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

    def unordered_completion_rate(self, task: ITask) -> float:
        """
        Calculate the unordered completion rate of the given Task from the Actions in the Sequence.

        :param task: The Task to cross-reference UserActions against.
        """
        return unordered_task_completion_rate(task, self)

    def ordered_completion_rate(self, task: ITask) -> float:
        """
        Calculate the ordered completion rate of the given Task from the Actions in the Sequence.

        :param task: The Task to cross-reference UserActions against.
        """
        return ordered_task_completion_rate(task, self)

    def location_ids(self) -> Set[str]:
        """
        Return a set of the ids of the unique locations visited in the sequence.
        """
        if self._location_ids is None:
            location_ids = set()
            for action in self._user_actions:
                location_ids.add(action.source_id)
                if action.target_id:
                    location_ids.add(action.target_id)
            self._location_ids = location_ids
        return self._location_ids

    def contains_location_id(self, location_id: str) -> bool:
        """
        Determine whether the location was visited in the sequence.
        """
        return location_id in self.location_ids()

    def action_types(self) -> Set[str]:
        """
        Return a set of the unique action types carried out in the sequence.
        """
        return set([action.action_type for action in self])

    def back_click_rates(self) -> Dict[IActionTemplate, float]:

        rates = {}
        template_list = self.action_templates()
        for template in self.action_template_set():
            forwards = template_list.count(template)
            backwards = template_list.count(template.reversed())
            rate = backwards / forwards
            if rate <= 1:
                rates[template] = rate
        return rates

    def dwell_times(self, sum_by_location: bool) -> Dict[str, Union[timedelta, List[timedelta]]]:
        """
        Return the amount of time spent by the user at each location.

        :param sum_by_location: Whether to sum the durations of time spent at each location or keep as a list.
        """
        if sum_by_location:
            dwell_times = defaultdict(timedelta)
            for a in range(1, len(self)):
                prev_action = self[a - 1]
                next_action = self[a]
                if notnull(prev_action.target_id) and prev_action.target_id != '':
                    location = prev_action.target_id
                else:
                    location = prev_action.source_id
                dwell_times[location] += next_action.time_stamp - prev_action.time_stamp
        else:
            dwell_times = defaultdict(list)
            for a in range(1, len(self)):
                prev_action = self[a - 1]
                next_action = self[a]
                if notnull(prev_action.target_id) and prev_action.target_id != '':
                    location = prev_action.target_id
                else:
                    location = prev_action.source_id
                dwell_times[location].append(
                    next_action.time_stamp - prev_action.time_stamp
                )
        return dwell_times

    def __getitem__(self, item) -> IUserAction:

        return self._user_actions[item]

    def __repr__(self) -> str:

        return 'ActionSequence([{}])'.format(
            len(self._user_actions)
        )

    def __len__(self) -> int:

        return len(self._user_actions)

    def __contains__(self, item) -> bool:

        if isinstance(item, IUserAction):
            return item in self._user_actions
        elif isinstance(item, IActionTemplate):
            return item in self.action_templates()
        else:
            raise TypeError('item must be IUserAction or IActionTemplate')

    def __iter__(self) -> Iterator[IUserAction]:

        return self._user_actions.__iter__()


def _create_action_template_condition(value: Union[IActionTemplate, FunctionType]) -> FunctionType:

    def action_template_condition(template: IActionTemplate):
        if template == value:
            return True
        else:
            return False

    if isinstance(value, IActionTemplate):
        return action_template_condition
    elif isinstance(value, FunctionType):
        return value
    else:
        raise TypeError('expected IActionTemplate or FunctionType')

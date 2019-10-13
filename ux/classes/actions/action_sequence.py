from datetime import timedelta
from typing import List, Callable

from ux.calcs.object_calcs.efficiency import lostness
from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate, \
    binary_task_success
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.tasks.i_task import ITask
from ux.interfaces.actions.i_user_action import IUserAction


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
        return [
            user_action.template()
            for user_action in self._user_actions
        ]

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

    def duration(self):
        """
        Return the total duration of the ActionSequence from the first Action to the last.

        :rtype: timedelta
        """
        start_time = self.user_actions[0].time_stamp
        end_time = self.user_actions[-1].time_stamp
        return end_time - start_time

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

    def split_after(self, condition: Callable[[IUserAction], bool], copy_meta: bool):
        """
        Split into a list of new ActionSequences after each `UserAction` where `condition` is met.

        :param condition: Lambda function to test when to break the sequence.
        :param copy_meta: Whether to copy the `meta` dict into the new Sequences.
        :rtype: List[IActionSequence]
        """
        new_sequences = []
        sequence_actions = []
        for a, action in enumerate(self.user_actions):
            sequence_actions.append(action)
            if condition(action):
                new_sequences.append(ActionSequence(
                    user_actions=sequence_actions,
                    meta=self.meta.copy() if copy_meta else None
                ))
                sequence_actions = []
        return new_sequences

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
        location_ids = set()
        for action in self._user_actions:
            location_ids.add(action.source_id)
            if action.target_id:
                location_ids.add(action.target_id)
        return location_ids

    def action_types(self):
        """
        Return a set of the unique action types carried out in the sequence.

        :rtype: Set[str]
        """
        return set([action.action_type for action in self.user_actions])

    def __repr__(self):

        return 'ActionSequence([{}])'.format(
            len(self._user_actions)
        )

    def __len__(self):

        return len(self._user_actions)

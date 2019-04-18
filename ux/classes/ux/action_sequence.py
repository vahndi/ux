from datetime import timedelta
from typing import List, Callable

from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate, \
    binary_task_success
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.ux.i_action_sequence import IActionSequence
from ux.interfaces.ux.i_task import ITask
from ux.interfaces.ux.i_user_action import IUserAction
from ux.interfaces.ux.i_action_template import IActionTemplate


class ActionSequence(IActionSequence):
    """
    Represents a sequence of UserActions taken by a User.
    """
    def __init__(self, user_actions: List[IUserAction] = None, extra: dict = None):
        """
        Create a new ActionSequence.

        :param user_actions: List of Actions to use to construct the ActionSequence.
        :param extra: Optional additional data to store with the ActionSequence.
        """
        self._user_actions = user_actions or []
        self._extra = extra

    @property
    def user_actions(self):
        """
        Return the list of UserActions in the ActionSequence.

        :rtype: List[IUserAction]
        """
        return self._user_actions

    @property
    def extra(self):
        """
        Return the dictionary of extra information added at construction time.

        :rtype: dict
        """
        return self._extra

    def action_templates(self):
        """
        Return a list of ActionTemplates derived from each of the UserActions taken.

        :rtype: List[IActionTemplate]
        """
        return [
            user_action.template()
            for user_action in self._user_actions
        ]

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

    def split_after(self, condition: Callable[[IUserAction], bool], copy_extra: bool):
        """
        Split into a list of new ActionSequences after each `UserAction` where `condition` is met.

        :param condition: Lambda function to test when to break the sequence.
        :param copy_extra: Whether to copy the `extra` dict into the new Sequences.
        :rtype: List[IActionSequence]
        """
        new_sequences = []
        sequence_actions = []
        for a, action in enumerate(self.user_actions):
            sequence_actions.append(action)
            if condition(action):
                new_sequences.append(ActionSequence(
                    user_actions=sequence_actions,
                    extra=self.extra.copy() if copy_extra else None
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

    def __repr__(self):

        return 'ActionSequence([{}])'.format(
            len(self._user_actions)
        )

    def __len__(self):

        return len(self._user_actions)

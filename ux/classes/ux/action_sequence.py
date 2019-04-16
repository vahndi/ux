from typing import List

from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.ux.i_action_sequence import IActionSequence
from ux.interfaces.ux.i_task import ITask
from ux.interfaces.ux.i_user_action import IUserAction
from ux.interfaces.ux.i_action_template import IActionTemplate


class ActionSequence(IActionSequence):

    def __init__(self, user_actions: List[IUserAction] = None, extra: dict = None):

        self._user_actions = user_actions or []
        self._extra = extra

    @property
    def user_actions(self):
        """
        :rtype: List[IUserAction]
        """
        return self._user_actions

    @property
    def extra(self):
        return self._extra

    def action_templates(self):
        """
        :rtype: List[IActionTemplate]
        """
        return [
            user_action.template()
            for user_action in self._user_actions
        ]

    def duration(self):

        start_time = self.user_actions[0].time_stamp
        end_time = self.user_actions[-1].time_stamp
        return end_time - start_time

    def intersects_task(self, task: ITask):
        """
        :rtype: bool
        """
        return sequence_intersects_task(action_sequence=self, task=task)

    def split_after(self, condition: callable, copy_extra: bool):
        """
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

    def __repr__(self):

        return 'ActionSequence([{}])'.format(
            len(self._user_actions)
        )

    def __len__(self):

        return len(self._user_actions)

    def unordered_completion_rate(self, task: ITask):
        """
        :rtype: float
        """
        return unordered_task_completion_rate(task, self)

    def ordered_completion_rate(self, task: ITask):
        """
        :rtype: float
        """
        return ordered_task_completion_rate(task, self)


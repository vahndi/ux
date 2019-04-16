from typing import List

from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.ux.i_action_sequence import IActionSequence
from ux.interfaces.ux.i_action_template import IActionTemplate
from ux.interfaces.ux.i_task import ITask


class Task(ITask):

    def __init__(self, name: str, action_templates: List[IActionTemplate] = None):

        self._name = name
        self._action_templates = action_templates or []

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @property
    def action_templates(self):
        """
        :rtype: List[IActionTemplate]
        """
        return self._action_templates

    def add_action_template(self, action_template: IActionTemplate):

        self._action_templates.append(action_template)

    def unordered_completion_rate(self, action_sequence: IActionSequence):
        """
        :rtype: float
        """
        return unordered_task_completion_rate(self, action_sequence)

    def ordered_completion_rate(self, action_sequence: IActionSequence):
        """
        :rtype: float
        """
        return ordered_task_completion_rate(self, action_sequence)

    def intersects_sequence(self, action_sequence):
        """
        :rtype: bool
        """
        return sequence_intersects_task(action_sequence=action_sequence, task=self)

    def __len__(self):

        return len(self._action_templates)

    def __repr__(self):

        return 'Task({} [{}])'.format(
            self._name, len(self._action_templates)
        )

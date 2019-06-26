from typing import List, Callable

from ux.calcs.object_calcs.efficiency import lostness
from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate, \
    binary_task_success
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.tasks.i_task import ITask


class Task(ITask):
    """
    Represents a Task corresponding to a sequence of desirable Actions.
    """
    def __init__(self, name: str, action_templates: List[IActionTemplate] = None):
        """
        Create a new Task.

        :param name: The name of the new Task.
        :param action_templates: A list of ActionTemplates that compose the Task.
        """
        self._name = name
        self._action_templates = action_templates or []

    @property
    def name(self):
        """
        Return the name of the Task.

        :rtype: str
        """
        return self._name

    @property
    def action_templates(self):
        """
        Return the list of ActionTemplates that compose the Task.

        :rtype: List[IActionTemplate]
        """
        return self._action_templates

    def add_action_template(self, action_template: IActionTemplate):
        """
        Add a new ActionTemplate to the end of the Task.

        :param action_template: The ActionTemplate to add.
        """
        self._action_templates.append(action_template)

    def unordered_completion_rate(self, action_sequence: IActionSequence):
        """
        Calculate the unordered completion rate of the Task from the Actions in the given ActionSequence.

        :rtype: float
        """
        return unordered_task_completion_rate(self, action_sequence)

    def ordered_completion_rate(self, action_sequence: IActionSequence):
        """
        Calculate the ordered completion rate of the Task from the Actions in the given ActionSequence.

        :rtype: float
        """
        return ordered_task_completion_rate(self, action_sequence)

    def intersects_sequence(self, action_sequence: IActionSequence):
        """
        Return True if the given ActionSequence has any ActionTemplates that are equivalent to any Actions in the Task.

        :rtype: bool
        """
        return sequence_intersects_task(action_sequence=action_sequence, task=self)

    def binary_task_success(self, action_sequence: IActionSequence,
                            success_func: Callable[[ITask, IActionSequence], bool]):
        """
        Return True if success_func is met.

        :param action_sequence: The ActionSequence to assess success of.
        :param success_func: Callable to use to assess success.
        :rtype: bool
        """
        return binary_task_success(
            task=self, action_sequence=action_sequence,
            success_func=success_func
        )

    def lostness(self, action_sequence: IActionSequence):
        """
        Return the lostness of the given ActionSequence with respect to this Task.

        :param action_sequence: The ActionSequence to calculate lostness for.
        :rtype: float
        """
        return lostness(task=self, action_sequence=action_sequence)

    def __len__(self):

        return len(self._action_templates)

    def __repr__(self):

        return 'Task({} [{}])'.format(
            self._name, len(self._action_templates)
        )

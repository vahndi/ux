from typing import List, Callable, Iterator

from ux.calcs.object_calcs.efficiency import lostness
from ux.calcs.object_calcs.task_success import unordered_task_completion_rate, ordered_task_completion_rate, \
    binary_task_success
from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.sequences.i_action_sequence import IActionSequence
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
        self._name: str = name
        self._action_templates: List[IActionTemplate] = action_templates or []

    @property
    def name(self) -> str:
        """
        Return the name of the Task.
        """
        return self._name

    @property
    def action_templates(self) -> List[IActionTemplate]:
        """
        Return the list of ActionTemplates that compose the Task.
        """
        return self._action_templates

    def add_action_template(self, action_template: IActionTemplate):
        """
        Add a new ActionTemplate to the end of the Task.

        :param action_template: The ActionTemplate to add.
        """
        self._action_templates.append(action_template)

    def unordered_completion_rate(self, action_sequence: IActionSequence) -> float:
        """
        Calculate the unordered completion rate of the Task from the Actions in the given ActionSequence.
        """
        return unordered_task_completion_rate(self, action_sequence)

    def ordered_completion_rate(self, action_sequence: IActionSequence) -> float:
        """
        Calculate the ordered completion rate of the Task from the Actions in the given ActionSequence.
        """
        return ordered_task_completion_rate(self, action_sequence)

    def intersects_sequence(self, action_sequence: IActionSequence) -> bool:
        """
        Return True if the given ActionSequence has any ActionTemplates that are equivalent to any Actions in the Task.
        """
        return sequence_intersects_task(action_sequence=action_sequence, task=self)

    def binary_task_success(self, action_sequence: IActionSequence,
                            success_func: Callable[[ITask, IActionSequence], bool]) -> bool:
        """
        Return True if success_func is met.

        :param action_sequence: The ActionSequence to assess success of.
        :param success_func: Callable to use to assess success.
        """
        return binary_task_success(
            task=self, action_sequence=action_sequence,
            success_func=success_func
        )

    def lostness(self, action_sequence: IActionSequence) -> float:
        """
        Return the lostness of the given ActionSequence with respect to this Task.

        :param action_sequence: The ActionSequence to calculate lostness for.
        """
        return lostness(task=self, action_sequence=action_sequence)

    def __len__(self) -> int:

        return len(self._action_templates)

    def __repr__(self) -> str:

        return 'Task({} [{}])'.format(
            self._name, len(self._action_templates)
        )

    def __getitem__(self, item) -> IActionTemplate:

        return self._action_templates[item]

    def __contains__(self, item) -> bool:

        if isinstance(item, IActionTemplate):
            return item in self._action_templates
        else:
            raise TypeError('item must be IActionTemplate')

    def __iter__(self) -> Iterator[IActionTemplate]:

        return self._action_templates.__iter__()

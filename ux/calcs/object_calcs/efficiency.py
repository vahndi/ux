from math import sqrt

from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.tasks.i_task import ITask


def lostness(task: ITask, action_sequence: IActionSequence):
    """
    Calculate the `lostness` metric for the given ActionSequence, using the Task as a reference.

    :param task: The Task to use to find the optimum number of Actions.
    :param action_sequence: The ActionSequence to use to find the unique and total number of Actions.
    :rtype: float
    """
    task_templates = task.action_templates
    assert len(task_templates) == len(set(task_templates)), \
        'Task contains repeated ActionTemplates'
    optimum = len(task.action_templates)
    sequence_templates = action_sequence.action_templates()
    unique = len(set(sequence_templates))
    total = len(sequence_templates)
    return sqrt(
        (unique / total - 1) ** 2 +
        (optimum / unique - 1) ** 2
    )

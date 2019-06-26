from typing import Tuple

from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.tasks.i_task import ITask


def task_extents(action_sequence: IActionSequence, task: ITask):
    """
    Return the start and end index of the actions in the sequence that are part of the task.

    :return: Index of the first and last User Actions in the Sequence that are also in the Task.
    :rtype: Tuple[int, int]
    """
    i_first = 0
    i_last = len(action_sequence) - 1
    sequence_templates = action_sequence.action_templates()
    while sequence_templates[i_first] not in task.action_templates:
        i_first += 1
    while sequence_templates[i_last] not in task.action_templates:
        i_last -= 1
    return i_first, i_last


def time_on_task(task: ITask, action_sequence: IActionSequence):
    """
    Measure the time from the start of the first action in the task to the end of the last action.

    :param task: Task definition.
    :param action_sequence: Sequence of actions
    """
    i_first, i_last = task_extents(action_sequence=action_sequence, task=task)
    first_action = action_sequence.user_actions[i_first]
    last_action = action_sequence.user_actions[i_last]
    return last_action.time_stamp - first_action.time_stamp

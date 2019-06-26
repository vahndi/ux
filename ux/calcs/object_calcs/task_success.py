from typing import Callable

from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.tasks.i_task import ITask


def unordered_task_completion_rate(task: ITask, action_sequence: IActionSequence):
    """
    Calculate the Task completion from a Sequence of User Actions.
    Does not require the Actions to be completed in order.

    :param task: The Task to measure completion rate for.
    :param action_sequence: The Sequence of user actions.
    :rtype: float
    """
    # calculate sum of task unique action template weights
    task_templates = task.action_templates
    task_template_set = set(task_templates)
    task_weight = sum([action_template.weighting
                       for action_template in task.action_templates])
    # calculate sum of weights of action templates in task and sequence
    sequence_template_set = set(action_sequence.action_templates())
    overlaps = task_template_set.intersection(sequence_template_set)
    overlap_weight = sum([
        action_template.weighting
        for action_template in overlaps
    ])
    return overlap_weight / task_weight


def ordered_task_completion_rate(task: ITask, action_sequence: IActionSequence):
    """
    Calculate the Task completion from a sequence of User Actions.
    Requires that the Actions are completed in the order specified in the Task.

    :param task: The Task to measure completion rate for.
    :param action_sequence: The Sequence of User Actions
    :rtype: float
    """
    # calculate sum of task action template weights
    task_templates = task.action_templates
    task_weight = sum([action_template.weighting
                       for action_template in task.action_templates])
    num_templates = len(task_templates)
    sequence_templates = action_sequence.action_templates()
    # find weights of action templates in sequence in order
    found = True
    num_found = 0
    sequence_weight = 0.0
    while found and num_found < num_templates:
        search_template = task_templates[num_found]
        try:
            sequence_index = sequence_templates.index(search_template)
            num_found += 1
            sequence_weight += search_template.weighting
            sequence_templates = sequence_templates[sequence_index + 1:]
        except:
            found = False

    return sequence_weight / task_weight


def binary_task_success(task: ITask, action_sequence: IActionSequence,
                        success_func: Callable[[ITask, IActionSequence], bool]):
    """
    Calculate the binary task success for each sequence.

    :param task: The Task to assess success against.
    :param action_sequence: ActionSequence to assess success of.
    :param success_func: Callable to use to assess success.
    :return: List of False for fail or True for pass
    :rtype: bool
    """
    return success_func(task, action_sequence)

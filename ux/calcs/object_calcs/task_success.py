from ux.interfaces.ux.i_action_sequence import IActionSequence
from ux.interfaces.ux.i_task import ITask


def unordered_task_completion_rate(task: ITask, action_sequence: IActionSequence):
    """
    Calculate the Task completion from a Sequence of User Actions.
    Does not require the Actions to be completed in order.

    :param task: The Task to measure completion rate for.
    :param action_sequence: The Sequence of user actions.
    :rtype: float
    """
    task_template_set = set(task.action_templates)
    num_task_actions = len(task_template_set)
    session_template_set = set(action_sequence.action_templates())
    num_overlaps = len(task_template_set.intersection(session_template_set))
    return num_overlaps / num_task_actions


def ordered_task_completion_rate(task: ITask, action_sequence: IActionSequence):
    """
    Calculate the Task completion from a sequence of User Actions.
    Requires that the Actions are completed in the order specified in the Task.

    :param task: The Task to measure completion rate for.
    :param action_sequence: The Sequence of User Actions
    :rtype: float
    """
    task_templates = task.action_templates
    num_templates = len(task_templates)
    session_templates = action_sequence.action_templates()
    found = True
    num_found = 0
    while found and num_found < num_templates:
        search_value = task_templates[num_found]
        try:
            session_index = session_templates.index(search_value)
            num_found += 1
            session_templates = session_templates[session_index + 1:]
        except:
            found = False

    return num_found / num_templates



from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.tasks.i_task import ITask


def sequence_intersects_task(action_sequence: IActionSequence, task: ITask) -> bool:
    """
    Determine if the actions in the sequence intersect with those in the task.
    """
    sequence_template_set = set(action_sequence.action_templates())
    task_template_set = set(task.action_templates)
    return len(sequence_template_set.intersection(task_template_set)) > 0

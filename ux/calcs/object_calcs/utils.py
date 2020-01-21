from ux.sequences.action_sequence import ActionSequence
from ux.tasks.task import Task


def sequence_intersects_task(action_sequence: ActionSequence, task: Task) -> bool:
    """
    Determine if the actions in the sequence intersect with those in the task.
    """
    sequence_template_set = set(action_sequence.action_templates())
    task_template_set = set(task.action_templates)
    return len(sequence_template_set.intersection(task_template_set)) > 0

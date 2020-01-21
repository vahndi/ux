from collections import defaultdict
from typing import List, Dict

from ux.calcs.object_calcs.utils import sequence_intersects_task
from ux.sequences.action_sequence import ActionSequence
from ux.tasks.task import Task, TaskPair
from ux.actions.action_template import ActionTemplatePair


def transition_counts(task: Task, action_sequences: List[ActionSequence]) -> Dict[ActionTemplatePair, int]:
    """
    Count the transitions between actions.

    :param task: The task defining the actions that should  be counted.
    :param action_sequences: List of action sequences to count over.
    :return: Dictionary of {(from, to) => count}
    """
    transitions = defaultdict(int)
    task_action_set = set(task.action_templates)
    # count transitions
    for sequence in action_sequences:
        if not sequence_intersects_task(action_sequence=sequence, task=task):
            continue
        for a in range(len(sequence) - 1):
            from_action = sequence[a].template()
            to_action = sequence[a + 1].template()
            if {from_action, to_action}.issubset(task_action_set):
                transitions[(from_action, to_action)] += 1
    return transitions


def transition_probabilities(task: Task, action_sequences: List[ActionSequence]) -> Dict[TaskPair, float]:
    """
    Calculate the conditional probability of a first-order Markov Chain between actions.

    :param task: The task defining the actions that should  be counted.
    :param action_sequences: List of action sequences to count over.
    :return: Dictionary of {(from, to) => p(to|from)}
    """
    transitions = defaultdict(int)
    source_counts = defaultdict(int)
    task_action_set = set(task.action_templates)
    # count transitions and occurrences
    for sequence in action_sequences:
        if not sequence_intersects_task(action_sequence=sequence, task=task):
            continue
        for a in range(len(sequence) - 1):
            from_action = sequence[a].template()
            to_action = sequence[a + 1].template()
            if {from_action, to_action}.issubset(task_action_set):
                transitions[(from_action, to_action)] += 1
                source_counts[from_action] += 1
    # calculate conditional probabilities
    transition_probs = {}
    for (from_state, to_state), count in transitions.items():
        transition_probs[(from_state, to_state)] = (
                transitions[(from_state, to_state)] /
                source_counts[from_state]
        )

    return transition_probs

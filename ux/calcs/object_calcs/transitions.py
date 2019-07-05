from collections import defaultdict
from typing import List

from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.tasks.i_task import ITask


def transition_counts(task: ITask, action_sequences: List[IActionSequence]):
    """
    Count the transitions between actions.

    :param task: The task defining the actions that should  be counted.
    :param action_sequences: List of action sequences to count over.
    :return: Dictionary of {(from, to) => count}
    :rtype: Dict[Tuple[IActionTemplate, IActionTemplate], int]
    """
    transitions = defaultdict(int)
    task_action_set = set(task.action_templates)
    # count transitions
    for sequence in action_sequences:
        if not task.intersects_sequence(sequence):
            continue
        for a in range(len(sequence) - 1):
            from_action = sequence.user_actions[a].template()
            to_action = sequence.user_actions[a + 1].template()
            if {from_action, to_action}.issubset(task_action_set):
                transitions[(from_action, to_action)] += 1
    return transitions


def transition_probabilities(task: ITask, action_sequences: List[IActionSequence]):
    """
    Calculate the conditional probability of a first-order Markov Chain between actions.

    :param task: The task defining the actions that should  be counted.
    :param action_sequences: List of action sequences to count over.
    :return: Dictionary of {(from, to) => p(to|from)}
    :rtype: Dict[Tuple[ITask, ITask], float]
    """
    transitions = defaultdict(int)
    source_counts = defaultdict(int)
    task_action_set = set(task.action_templates)
    # count transitions and occurrences
    for sequence in action_sequences:
        if not task.intersects_sequence(sequence):
            continue
        for a in range(len(sequence) - 1):
            from_action = sequence.user_actions[a].template()
            to_action = sequence.user_actions[a + 1].template()
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

from collections import defaultdict
from pandas import Series, pivot_table, DataFrame
from typing import List

from interfaces.actions.i_action_sequence import IActionSequence


def count_transitions(action_sequences):
    """
    Count the transitions  from each action to each other action in the given sequences.

    :param action_sequences: List of IActionSequence to count transitions in.
    :type action_sequences: List[IActionSequence]
    :return: Dictionary of {(from, to) => count}
    :rtype: Dict[Tuple[IActionTemplate, IActionTemplate], int]
    """
    transitions = defaultdict(int)
    # count transitions
    for sequence in action_sequences:
        for a in range(len(sequence) - 1):
            from_action = sequence.user_actions[a].template()
            to_action = sequence.user_actions[a + 1].template()
            transitions[(from_action, to_action)] += 1
    return transitions


def create_transition_matrix(transitions: dict, get_name: callable = None,
                             order_by: str = 'from', exclude: List[str] = None):
    """
    Create a matrix from a dictionary of transition counts.

    :param transitions: Dictionary of transitions and their counts or probabilities.
    :type transitions: Dict[Tuple[object, object], Union[float, int]]
    :param get_name: Optional lambda function to call to convert states to labels.
    :param order_by: Order labels by descending count of `from` or `to`.
    :param exclude: Optional list of labels to exclude from the plots.
    :rtype: DataFrame
    """
    get_name = get_name if get_name is not None else lambda a: a.source_id
    transitions = Series(transitions).reset_index()
    transitions.columns = ['from', 'to', 'count']
    transitions['from'] = transitions['from'].map(get_name)
    transitions['to'] = transitions['to'].map(get_name)
    if exclude is not None:
        transitions = transitions.loc[
            (~transitions['from'].isin(exclude)) &
            (~transitions['to'].isin(exclude))
        ]
    order_names = transitions.groupby(order_by).sum()['count'].sort_values(ascending=False).index.tolist()
    matrix = pivot_table(
        data=transitions, values='count',
        index='to', columns='from'
    )
    matrix = matrix.loc[order_names]
    matrix = matrix[order_names]
    return matrix


def order_locations_by_transition_frequency(sequences: List[IActionSequence]):
    
    counts = count_transitions(sequences)
    print(counts)
    
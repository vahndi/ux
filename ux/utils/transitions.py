from collections import defaultdict
from pandas import Series, pivot_table, DataFrame, notnull
from typing import List

from ux.interfaces.sequences.i_action_sequence import IActionSequence


def count_action_transitions(action_sequences):
    """
    Count the transitions from each action to each other action in the given sequences.

    :param action_sequences: List of IActionSequence to count transitions in.
    :type action_sequences: List[IActionSequence]
    :return: Dictionary of {(from, to) => count}
    :rtype: dict[tuple[IActionTemplate, IActionTemplate], int]
    """
    transitions = defaultdict(int)
    # count transitions
    for sequence in action_sequences:
        for a in range(len(sequence) - 1):
            from_action = sequence.user_actions[a].template()
            to_action = sequence.user_actions[a + 1].template()
            transitions[(from_action, to_action)] += 1
    return transitions


def count_location_transitions(action_sequences):
    """
    Count the transitions from each location to each other location in actions in the given sequences.

    :param action_sequences: List of IActionSequence to count transitions in.
    :type action_sequences: List[IActionSequence]
    :rtype: dict[tuple[str, str], int]
    """
    transitions = defaultdict(int)
    # count transitions
    for sequence in action_sequences:
        for action in sequence.user_actions:
            source = action.source_id
            target = action.target_id
            if notnull(source) and notnull(target):
                transitions[(source, target)] += 1
    return transitions


def create_transition_table(transitions: dict, get_name=None, exclude=None):
    """
    Create a DataFrame of transitions with columns ['from', 'to', 'count']

    :param transitions: Dictionary of transitions and their counts or probabilities.
    :type transitions: Dict[Tuple[object, object], Union[float, int]]
    :param get_name: Optional lambda function to call to convert states to labels.
    :type get_name: Callable[[IUserAction], str]
    :param exclude: Optional list of names to exclude from the table.
    :type exclude: Union[str, List[str]]
    :rtype: DataFrame
    """
    get_name = get_name if get_name is not None else lambda action: action.source_id
    transitions = Series(transitions).reset_index()
    transitions.columns = ['from', 'to', 'count']
    transitions = transitions.loc[
        (transitions['from'].notnull()) &
        (transitions['to'].notnull())
    ]
    transitions['from'] = transitions['from'].map(get_name)
    transitions['to'] = transitions['to'].map(get_name)
    if exclude is not None:
        if type(exclude) is str:
            exclude = [exclude]
        transitions = transitions.loc[
            (~transitions['from'].isin(exclude)) &
            (~transitions['to'].isin(exclude))
        ]
    return transitions


def create_transition_matrix(transitions: dict, get_name=None,
                             order_by='from', exclude=None):
    """
    Create a transition matrix from a dictionary of transition counts.

    :param transitions: Dictionary of transitions and their counts or probabilities.
    :type transitions: Dict[Tuple[object, object], Union[float, int]]
    :param get_name: Optional lambda function to call to convert states to labels.
    :type get_name: Callable[[IUserAction], str]
    :param order_by: Order labels by descending count of `from` or `to`, or pass a list to set order explicitly.
    :type order_by: Union[str, List[str]]
    :param exclude: Optional list of labels to exclude from the plots.
    :type exclude: Union[str, List[str]]
    :rtype: DataFrame
    """
    transitions = create_transition_table(transitions=transitions, get_name=get_name, exclude=exclude)
    if type(order_by) is str:
        order_names = transitions.groupby(order_by).sum()['count'].sort_values(ascending=False).index.tolist()
    else:
        order_names = order_by
    matrix = pivot_table(
        data=transitions, values='count',
        index='to', columns='from'
    )
    matrix = matrix.loc[filter(lambda n: n in matrix.index, order_names)]
    matrix = matrix[filter(lambda n: n in matrix.columns, order_names)]
    return matrix


def find_most_probable_sequence(transitions, get_name=None, exclude=None, start_at: str = None):
    """
    Find the most probable transition sequence.

    :param transitions: Dictionary of transitions and their counts or probabilities.
    :type transitions: Dict[Tuple[object, object], Union[float, int]]
    :param get_name: Optional lambda function to call to convert states to labels.
    :type get_name: Callable[[IUserAction], str]
    :param exclude: Optional list of names to exclude from the sequence.
    :type exclude: Union[str, List[str]]
    :param start_at: Optional name of start state. Leave as None to use most common state.
    :rtype: List[str]
    """
    transitions = create_transition_table(transitions=transitions, get_name=get_name, exclude=exclude)
    # find most frequent from point
    if start_at is not None:
        current_name = start_at
    else:
        current_name = transitions.groupby('from').sum()['count'].sort_values(ascending=False).index[0]
    sequence = [current_name]
    # iteratively find most frequent transition point from the current point
    found = True
    while found:
        transitions = transitions.loc[transitions['to'] != current_name]
        if current_name in transitions['from'].tolist():
            current_name = transitions.loc[
                transitions['from'] == current_name
            ].sort_values('count', ascending=False).iloc[0]['to']
            if current_name not in sequence:
                sequence.append(current_name)
            else:
                found = False
        else:
            found = False
    return sequence

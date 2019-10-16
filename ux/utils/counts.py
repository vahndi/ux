from collections import defaultdict
from typing import List, Dict

from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.actions.i_user_action import IUserAction
from ux.classes.counts.count_config import CountConfig
from ux.classes.counts.temporal_count import TemporalCount


def count_actions_where(sequences: List[IActionSequence],
                        action_condition: callable(IUserAction),
                        sequence_condition: callable(IActionSequence) = None,
                        split_by: callable = None):
    """
    Count the number of UserActions in the ActionSequences where the given condition is True.

    :param sequences: The list of IActionSequences to test.
    :param action_condition: Condition to evaluate each user against.
    :param sequence_condition: Optional condition to evaluate each sequence against before checking action_condition.
    :param split_by: Optional callable to split counts by some attribute of each action.
    """
    # allow all sequences through if no sequence condition is specified
    if sequence_condition is None:
        sequence_condition = lambda seq: True
    if split_by is None:
        count = 0
        for sequence in sequences:
            if sequence_condition(sequence):
                for action in sequence.user_actions:
                    if action_condition(action):
                        count += 1
        return count
    else:
        counts = defaultdict(int)
        for sequence in sequences:
            if sequence_condition(sequence):
                for action in sequence.user_actions:
                    if action_condition(action):
                        split_result = split_by(action)
                        if type(split_result) is list:
                            for result in split_result:
                                counts[result] += 1
                        else:
                            counts[split_result] += 1
        return dict(counts)


def count_sequences_where(sequences: List[IActionSequence], condition, split_by=None):
    """
    Count the number of ActionSequences in the list where the given condition is True.

    :param sequences: The list of IActionSequences to test.
    :param condition: The condition to evaluate each sequence against.
    :type condition: Callable[[IActionSequence], bool]
    :param split_by: Optional callable to split counts by some attribute of each sequence. Should return a string.
    :type split_by: Callable[[IActionSequence], str]
    :return: Integer count if split_by is None. Otherwise dict of {split_value: count}
    """
    if split_by is None:
        count = 0
        for sequence in sequences:
            if condition(sequence):
                count += 1
        return count
    else:
        counts = defaultdict(int)
        for sequence in sequences:
            if condition(sequence):
                counts[split_by(sequence)] += 1
        return dict(counts)


def temporal_counts_by_config(sequences: List[IActionSequence], configs: List[CountConfig],
                              temporal_split: callable):
    """
    Count metrics using the settings in a list of CountConfigs.

    :param sequences: List of ActionSequences containing actions to measure metrics.
    :param configs: List of CountConfigs defining the metrics to count.
    :rtype: Dict[str, TemporalCount]
    :return Dict[config.name, TemporalCount for config]
    """
    total_counts = dict()
    for config in configs:
        total_counts[config.name] = TemporalCount(config.name)
    sequence_groups = temporal_split(sequences)
    for sequence_date, date_sequences in sequence_groups.items():
        for config in configs:
            # count sequences
            if config.action_condition is None:
                counts = count_sequences_where(
                    sequences=date_sequences,
                    condition=config.sequence_condition,
                    split_by=config.sequence_split_by
                )
            # count actions
            else:
                counts = count_actions_where(
                    sequences=date_sequences,
                    sequence_condition=config.sequence_condition,
                    action_condition=config.action_condition,
                    split_by=config.action_split_by
                )
            total_counts[config.name][sequence_date] = counts

    return total_counts

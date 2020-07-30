from collections import Counter
from typing import Dict, List, Union, Callable

from ux.counts.count_config import CountConfig
from ux.counts.temporal_count import TemporalCount
from ux.sequences.action_sequence import ActionSequence, SequenceFilter, \
    SequenceGrouper
from ux.sequences.sequences import Sequences
from ux.actions.user_action import ActionCounter, ActionFilter


def count_actions_where(sequences: Sequences,
                        action_condition: ActionFilter,
                        sequence_condition: SequenceFilter = None,
                        split_by: ActionCounter = None):
    """
    Count the number of UserActions in the ActionSequences where the given
    condition is True.

    :param sequences: The list of IActionSequences to test.
    :param action_condition: Condition to evaluate each user against.
    :param sequence_condition: Optional condition to evaluate each sequence
                               against before checking action_condition.
    :param split_by: Optional callable to split counts by some attribute of each
                     action.
    """
    # allow all sequences through if no sequence condition is specified
    sequences = sequences.filter(sequence_condition)
    if split_by is None:
        count = 0
        for sequence in sequences:
            count += sequence.count(action_condition)
        return count
    else:
        counts = Counter()
        for sequence in sequences:
            counts += sequence.filter(action_condition).counter(split_by)
        return dict(counts)


def count_sequences_where(sequences: Sequences,
                          condition: SequenceFilter, 
                          split_by: SequenceGrouper = None) -> Union[int, Dict[str, int]]:
    """
    Count the number of ActionSequences in the list where the given condition is
    True.

    :param sequences: The list of IActionSequences to test.
    :param condition: The condition to evaluate each sequence against.
    :param split_by: Optional callable to split counts by some attribute of each
                     sequence. Should return a string.
    :return: Integer count if split_by is None.
             Otherwise dict of {split_value: count}
    """
    if split_by is None:
        return sequences.count(condition)
    else:
        counts = sequences.filter(condition).counter(split_by)
        return dict(counts)


def temporal_counts_by_config(
        sequences: List[ActionSequence],
        configs: List[CountConfig],
        temporal_split: Callable[[List[ActionSequence]], List[ActionSequence]]
) -> Dict[str, TemporalCount]:
    """
    Count metrics using the settings in a list of CountConfigs.

    :param sequences: List of ActionSequences containing actions to measure
                      metrics.
    :param configs: List of CountConfigs defining the metrics to count.
    :param temporal_split: lambda function returning
                           OrderedDict[date, List[IActionSequence]]
    :return Dict[config.name, TemporalCount for config]
    """
    total_counts = dict()
    # create a new TemporalCount for each CountConfig
    for config in configs:
        total_counts[config.name] = TemporalCount(config.name)
    sequence_groups = temporal_split(sequences)
    for sequence_date, date_sequences in sequence_groups.items():
        for config in configs:
            # count sequences
            if config.action_condition is None:
                counts = count_sequences_where(
                    sequences=Sequences(date_sequences),
                    condition=config.sequence_condition,
                    split_by=config.sequence_split_by
                )
            # count actions
            else:
                counts = count_actions_where(
                    sequences=Sequences(date_sequences),
                    sequence_condition=config.sequence_condition,
                    action_condition=config.action_condition,
                    split_by=config.action_split_by
                )
            total_counts[config.name][sequence_date] = counts

    return total_counts

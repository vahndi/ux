from collections import Counter
from typing import Dict, List

from ux.classes.counts.count_config import CountConfig
from ux.classes.counts.temporal_count import TemporalCount
from ux.classes.sequences.sequences import Sequences
from ux.custom_types.action_types import ActionCounter, ActionFilter
from ux.custom_types.sequence_types import SequenceFilter, SequenceGrouper
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences


def count_actions_where(sequences: ISequences,
                        action_condition: ActionFilter,
                        sequence_condition: SequenceFilter = None,
                        split_by: ActionCounter = None):
    """
    Count the number of UserActions in the ActionSequences where the given condition is True.

    :param sequences: The list of IActionSequences to test.
    :param action_condition: Condition to evaluate each user against.
    :param sequence_condition: Optional condition to evaluate each sequence against before checking action_condition.
    :param split_by: Optional callable to split counts by some attribute of each action.
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


def count_sequences_where(sequences: ISequences, condition: SequenceFilter, split_by: SequenceGrouper = None):
    """
    Count the number of ActionSequences in the list where the given condition is True.

    :param sequences: The list of IActionSequences to test.
    :param condition: The condition to evaluate each sequence against.
    :type condition: SequenceFilter
    :param split_by: Optional callable to split counts by some attribute of each sequence. Should return a string.
    :return: Integer count if split_by is None. Otherwise dict of {split_value: count}
    """
    if split_by is None:
        return sequences.count(condition)
    else:
        counts = sequences.filter(condition).counter(split_by)
        return dict(counts)


def temporal_counts_by_config(sequences: List[IActionSequence], configs: List[CountConfig],
                              temporal_split) -> Dict[str, TemporalCount]:
    """
    Count metrics using the settings in a list of CountConfigs.

    :param sequences: List of ActionSequences containing actions to measure metrics.
    :param configs: List of CountConfigs defining the metrics to count.
    :param temporal_split: lambda function returning OrderedDict[date, List[IActionSequence]]
    :type temporal_split: Callable[[List[IActionSequence]], List[IActionSequence]]
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

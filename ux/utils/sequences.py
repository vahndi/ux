from collections import OrderedDict
from datetime import date, timedelta
from typing import List

from ux.interfaces.actions.i_action_sequence import IActionSequence


def split_sequences_by_day(sequences: List[IActionSequence],
                           start_date: date = None, end_date: date = None):
    """
    Split a list of ActionSequences into an OrderedDict mapping each date to a new list.

    Dates without any Sequences will contain an empty list.

    :param sequences: Original list of sequences to split by day.
    :param start_date: Optional first date to use to split the sequences.
    :param end_date: Optional last date to use.
    :rtype: OrderedDict[date, List[IActionSequence]]
    """
    min_date = None
    max_date = None
    if start_date is None or end_date is None:
        # find the min and max dates of each sequence start date time
        for sequence in sequences:
            sequence_date = sequence.user_actions[0].time_stamp.date()
            if min_date is None or sequence_date < min_date:
                min_date = sequence_date
            if max_date is None or sequence_date > max_date:
                max_date = sequence_date
    if start_date is None:
        start_date = min_date
    if end_date is None:
        end_date = max_date
    # build the lists of sequences
    current_date = start_date
    sequence_dict = OrderedDict()
    while current_date <= end_date:
        date_sequences = [
            sequence for sequence in sequences
            if sequence.user_actions[0].time_stamp.date() == current_date
        ]
        sequence_dict[current_date] = date_sequences
        current_date = current_date + timedelta(days=1)

    return sequence_dict


def count_sequences_where(sequences: List[IActionSequence], condition: callable(IActionSequence)):
    """
    Count the number of ActionSequences in the list where the given condition is True.

    :param sequences: The list of IActionSequences to test.
    :param condition: The condition to evaluate each condition against.
    :rtype: int
    """
    count = 0
    for sequence in sequences:
        if condition(sequence):
            count += 1
    return count

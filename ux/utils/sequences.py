from collections import OrderedDict
from datetime import date, timedelta
from typing import List, Tuple

from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.utils.dates import monday_on_or_before, monday_on_or_after, date_to_datetime


def get_sequence_start_end_dates(sequences: List[IActionSequence]):
    """
    Find the start and end dates of the sequences using the first UserAction in each sequence.

    :param sequences: List of IActionSequences to find dates from.
    :rtype: Tuple[date, date]
    """
    start_date = None
    end_date = None
    for sequence in sequences:
        sequence_date = sequence.user_actions[0].time_stamp.date()
        if start_date is None or sequence_date < start_date:
            start_date = sequence_date
        if end_date is None or sequence_date > end_date:
            end_date = sequence_date
    return start_date, end_date


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
    # get start and end dates
    min_date, max_date = get_sequence_start_end_dates(sequences)
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


def split_sequences_by_week(sequences: List[IActionSequence],
                            start_date: date = None, end_date: date = None):
    """
    Split a list of ActionSequences into an OrderedDict mapping each date to a new list.

    Dates without any Sequences will contain an empty list.

    :param sequences: Original list of sequences to split by day.
    :param start_date: Optional first date to use to split the sequences.
    :param end_date: Optional last date to use.
    :rtype: OrderedDict[date, List[IActionSequence]]
    """
    # get start and end dates
    min_date, max_date = get_sequence_start_end_dates(sequences)
    if start_date is None:
        start_date = min_date
    if end_date is None:
        end_date = max_date
    start_date = monday_on_or_before(start_date)
    end_date = monday_on_or_before(end_date)
    # build the lists of sequences
    current_date = start_date
    sequence_dict = OrderedDict()
    while current_date <= end_date:
        start_date_time = date_to_datetime(current_date)
        end_date_time = date_to_datetime(current_date + timedelta(days=7))
        date_sequences = [
            sequence for sequence in sequences
            if (
                    start_date_time <=
                    sequence.user_actions[0].time_stamp <
                    end_date_time
            )
        ]
        sequence_dict[current_date] = date_sequences
        current_date = current_date + timedelta(days=7)

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

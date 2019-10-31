from collections import OrderedDict
from datetime import date, timedelta, datetime
from typing import List, Tuple

from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.utils.dates import monday_on_or_before, date_to_datetime


def _get_sequence_start_end_dates(sequences: List[IActionSequence]):
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


def _get_sequence_start_end_date_times(sequences: List[IActionSequence]):
    """
    Find the start and end date-times of the sequences using the first UserAction in each sequence.

    :param sequences: List of IActionSequences to find dates from.
    :rtype: Tuple[datetime, datetime]
    """
    start_date_time = None
    end_date_time = None
    for sequence in sequences:
        sequence_date_time = sequence.user_actions[0].time_stamp
        if start_date_time is None or sequence_date_time < start_date_time:
            start_date_time = sequence_date_time
        if end_date_time is None or sequence_date_time > end_date_time:
            end_date_time = sequence_date_time
    return start_date_time, end_date_time


def split_sequences_by_hour(sequences: List[IActionSequence],
                            start_date_time: datetime = None, end_date_time: datetime = None):
    """
    Split a list of ActionSequences into an OrderedDict mapping each hour to a new list.

    Hours without any Sequences will contain an empty list.

    :param sequences: Original list of sequences to split by day.
    :param start_date_time: Optional first date-time to use to split the sequences.
    :param end_date_time: Optional last date-time to use.
    :rtype: OrderedDict[date, List[IActionSequence]]
    """
    if not sequences:
        return OrderedDict()
    # get start and end dates
    min_date, max_date = _get_sequence_start_end_date_times(sequences)
    if start_date_time is None:
        start_date_time = datetime(min_date.year, min_date.month, min_date.day,
                                   min_date.hour, 0, 0)
    if end_date_time is None:
        end_date_time = datetime(max_date.year, max_date.month, max_date.day,
                                 max_date.hour, 0, 0)
    # build the lists of sequences
    current_date_time = start_date_time
    sequence_dict = OrderedDict()
    while current_date_time <= end_date_time:
        date_sequences = [
            sequence for sequence in sequences
            if sequence.user_actions[0].time_stamp.date() == current_date_time.date() and
               sequence.user_actions[0].time_stamp.hour == current_date_time.hour
        ]
        sequence_dict[current_date_time] = date_sequences
        current_date_time = current_date_time + timedelta(hours=1)

    return sequence_dict


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
    if not sequences:
        return OrderedDict()
    # get start and end dates
    min_date, max_date = _get_sequence_start_end_dates(sequences)
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
    Split a list of ActionSequences into an OrderedDict mapping each week's start date to a new list.

    Dates without any Sequences will contain an empty list.

    :param sequences: Original list of sequences to split by day.
    :param start_date: Optional first date to use to split the sequences.
    :param end_date: Optional last date to use.
    :rtype: OrderedDict[date, List[IActionSequence]]
    """
    if not sequences:
        return OrderedDict()
    # get start and end dates
    min_date, max_date = _get_sequence_start_end_dates(sequences)
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
        first_date_time = date_to_datetime(current_date)
        last_date_time = date_to_datetime(current_date + timedelta(days=7))
        date_sequences = [
            sequence for sequence in sequences
            if (
                    first_date_time <=
                    sequence.user_actions[0].time_stamp <
                    last_date_time
            )
        ]
        sequence_dict[current_date] = date_sequences
        current_date = current_date + timedelta(days=7)

    return sequence_dict


def split_sequences_by_month(sequences: List[IActionSequence],
                             start_date: date = None, end_date: date = None):
    """
    Split a list of ActionSequences into an OrderedDict mapping each month's start date to a new list.

    Dates without any Sequences will contain an empty list.

    :param sequences: Original list of sequences to split by day.
    :param start_date: Optional first date to use to split the sequences.
    :param end_date: Optional last date to use.
    :rtype: OrderedDict[date, List[IActionSequence]]
    """
    if not sequences:
        return OrderedDict()
    # get start and end dates
    min_date, max_date = _get_sequence_start_end_dates(sequences)
    if start_date is None:
        start_date = min_date
    if end_date is None:
        end_date = max_date
    start_date = date(start_date.year, start_date.month, 1)
    end_date = date(end_date.year, end_date.month, 1)
    # build the lists of sequences
    current_date = start_date
    sequence_dict = OrderedDict()
    while current_date <= end_date:
        first_date = current_date
        last_date = (
            date(first_date.year, first_date.month + 1, 1)
            if first_date.month < 12
            else date(first_date.year + 1, 1, 1)
        )
        date_sequences = [
            sequence for sequence in sequences
            if first_date <= sequence.user_actions[0].time_stamp.date() < last_date
        ]
        sequence_dict[current_date] = date_sequences
        current_date = last_date

    return sequence_dict

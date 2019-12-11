from typing import Dict

from ux.classes.wrappers.map_result import MapResult
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences_group_by import ISequencesGroupBy


class ISequences(object):

    @property
    def sequences(self):
        """
        Return a list of the individual Sequences in the collection.

        :rtype: List[IActionSequence]
        """
        raise NotImplementedError

    def filter(self, condition):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def group_filter(self, filters):
        """
        :rtype: ISequencesGroupBy
        """
        raise NotImplementedError

    def count(self):
        """
        :rtype: int
        """
        raise NotImplementedError

    def copy(self):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def intersection(self, other):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    @staticmethod
    def intersect_all(sequences):
        """
        :type sequences: List[ISequences]
        :rtype: ISequences
        """
        raise NotImplementedError

    def back_click_rates(self):
        """
        :rtype: Dict[IActionTemplate, float]
        """
        raise NotImplementedError

    def group_by(self, by):
        """
        :rtype: ISequencesGroupBy
        """
        raise NotImplementedError

    @property
    def durations(self):
        """
        :rtype: List[timedelta]
        """
        raise NotImplementedError

    def action_template_counts(self):
        """
        :rtype: Dict[IActionTemplate, int]
        """
        raise NotImplementedError

    def action_template_sequence_counts(self):
        """
        Return a total count of the number of ActionSequences containing each ActionTemplate in the collection.

        :rtype: Dict[IActionTemplate, int]
        """
        raise NotImplementedError

    def action_template_transition_counts(self):
        """
        Return counts of transitions between pairs of Actions from each Sequence in the collection.

        :return: Dictionary of {(from, to) => count}
        :rtype: Dict[tuple[IActionTemplate, IActionTemplate], int]
        """
        raise NotImplementedError

    def location_transition_counts(self, exclude=None):
        """
        Count the transitions from each location to each other location in actions in the given sequences.

        :return: Counter[Tuple[from, to], count]
        :rtype: Counter[Tuple[str, str], int]
        """
        raise NotImplementedError

    def dwell_times(self, sum_by_location: bool, sum_by_sequence: bool):
        """
        Return the amount of time spent by the user at each location.

        :param sum_by_location: Whether to sum the durations of time spent at each location or keep as a list.
        :param sum_by_sequence: Whether to sum the durations of time spent at each location in each sequence or keep as a list.
        :rtype: Dict[str, Union[timedelta, List[timedelta]]]
        """
        raise NotImplementedError

    def map(self, mapper):
        """
        :rtype: MapResult
        """
        raise NotImplementedError

    def sort(self, by: str, ascending: bool = True):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def __getitem__(self, item):

        raise NotImplementedError

    def __len__(self):

        raise NotImplementedError

    def __contains__(self, item: IActionSequence):

        raise NotImplementedError

    def __iter__(self):
        """
        :rtype: IActionSequence
        """
        raise NotImplementedError

    def __add__(self, other):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def __sub__(self, other):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

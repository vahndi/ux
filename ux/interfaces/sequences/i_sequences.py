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

    def action_template_counts(self, rtype: type = dict):
        """
        :rtype: Dict[IActionTemplate, int]
        """
        raise NotImplementedError

    def action_template_sequence_counts(self, rtype: type = dict):
        """
        Return a total count of the number of ActionSequences containing each ActionTemplate in the collection.

        :rtype: Dict[IActionTemplate, int]
        """
        raise NotImplementedError

    def action_template_transition_counts(self, rtype: type = dict):
        """
        Return counts of transitions between pairs of Actions from each Sequence in the collection.

        :return: Dictionary of {(from, to) => count}
        :rtype: Dict[tuple[IActionTemplate, IActionTemplate], int]
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

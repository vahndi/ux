from typing import Dict, Callable

from ux.interfaces.sequences.i_action_sequence import IActionSequence


class ISequences(object):

    @property
    def sequences(self):
        """
        Return a list of the individual Sequences in the collection.

        :rtype: List[IActionSequence]
        """
        raise NotImplementedError

    def filter(self, condition: Callable[[IActionSequence], bool]):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def group_filter(self, filters: Dict[str, Callable[[IActionSequence], bool]]):
        """
        :rtype: SequencesGroupBy
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

    def map(self, mapper, rtype: type = dict):

        raise NotImplementedError

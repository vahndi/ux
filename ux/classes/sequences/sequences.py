from collections import defaultdict
from itertools import product
from types import FunctionType
from typing import List, Iterable, Callable, Any

from ux.classes.sequences.sequences_group_by import SequencesGroupBy
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences


class Sequences(ISequences):

    def __init__(self, sequences: List[IActionSequence]):
        """

        :param sequences:
        """
        self._sequences = sequences

    @property
    def sequences(self):

        return self._sequences

    def filter(self, condition: Callable[[IActionSequence], bool]):
        """
        Return a new Sequences containing only the sequences matching the `condition`.

        :param condition: lambda(sequence) that returns True include a sequence.
        :rtype: Sequences
        """
        filtered = []
        for sequence in self._sequences:
            if condition(sequence):
                filtered.append(sequence)
        return Sequences(filtered)

    def count(self):
        return len(self._sequences)

    def copy(self):
        """
        :rtype: ISequences
        """
        return Sequences(self._sequences)

    def intersection(self, other):
        """
        :type other: Union[Sequences, List[IActionSequence]]
        :rtype: Sequences
        """
        if type(other) is Sequences:
            other = other.sequences
        return Sequences(
            list(set(self._sequences).intersection(other))
        )

    @staticmethod
    def intersect_all(sequences):
        """
        :type sequences: List[ISequences]
        :rtype: ISequences
        """
        intersect = sequences[0].copy()
        for s in sequences[1:]:
            intersect = intersect.intersection(s)
        return intersect

    def group_by(self, by):
        """
        Return a SequencesGroupBy keyed by each value returned by a single grouper, or each combination of groupers
        for a list of groupers.
        Each grouper should be a lambda function that returns a picklable value e.g. str.

        :param by: lambda(sequence) or dict[group_name, lambda(sequence)] to calculate groupby.
        :type by: Union[Callable[[IActionSequence], Any], Dict[str, Union[Callable[[IActionSequence], Any]]
        :rtype: SequencesGroupBy
        """
        splits = defaultdict(list)
        if isinstance(by, FunctionType):
            for sequence in self._sequences:
                splits[by(sequence)].append(sequence)
            return SequencesGroupBy(data=dict([
                (group_name, Sequences(group_sequences))
                for group_name, group_sequences in splits.items()
            ]))
        elif isinstance(by, dict):
            group_by_names = sorted(by.keys())
            group_bys = {
                by_name: self.group_by(by[by_name])
                for by_name in group_by_names
            }
            result = dict()
            for subgroups_combo in product(*[group_bys[group].items() for group in group_bys.keys()]):
                result_key = tuple([subgroup[0] for subgroup in subgroups_combo])
                result_sequences = [subgroup[1] for subgroup in subgroups_combo]
                result[result_key] = Sequences.intersect_all(result_sequences)
            return SequencesGroupBy(result, names=group_by_names)

    def __repr__(self):

        return 'Sequences({})'.format(len(self._sequences))

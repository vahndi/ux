from typing import List

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

    def filter(self, condition: callable):
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

    @property
    def count(self):
        return len(self._sequences)

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


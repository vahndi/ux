from collections import defaultdict, OrderedDict
from itertools import product
from types import FunctionType
from typing import List, Dict, Callable

from pandas import DataFrame, MultiIndex

from ux.classes.sequences.sequences_group_by import SequencesGroupBy
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences
from ux.utils.misc import get_method_name


class Sequences(ISequences):

    def __init__(self, sequences: List[IActionSequence]):
        """
        :param sequences:
        """
        self._sequences = sequences

    @property
    def sequences(self):
        """
        :rtype: List[IActionSequence]
        """
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

    def group_filter(self, filters: Dict[str, Callable[[IActionSequence], bool]]):
        """
        Return a new SequencesGroupBy keyed by the dict key with values matching each filter.

        :param filters: dict[str, lambda(Sequence)]
        :rtype: SequencesGroupBy
        """
        filtered = {
            filter_name: self.filter(filter_condition)
            for filter_name, filter_condition in filters.items()
        }
        return SequencesGroupBy(data=filtered, names=['filter'])

    def count(self):
        """
        :rtype: int
        """
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
        Return a SequencesGroupBy keyed by each value returned by a single grouper,
        or each combination of groupers for a list of groupers.
        Each grouper should be a lambda function that returns a picklable value e.g. str.

        :param by: lambda(Sequence) or dict[group_name, lambda(Sequence)] or list[str or lambda(Sequence)].
        :type by: Union[Callable[[IActionSequence], Any], Dict[str, Union[Callable[[IActionSequence], Any]]
        :rtype: SequencesGroupBy
        """
        def apply_group_by(method):
            """
            :rtype: Dict[str, Sequences]
            """
            splits = defaultdict(list)
            for sequence in self._sequences:
                splits[method(sequence)].append(sequence)
            return {
                group_name: Sequences(group_sequences)
                for group_name, group_sequences in splits.items()
            }

        lookups = {
            'date': lambda seq: seq.start_date_time().date(),
            'start_date': lambda seq: seq.start_date_time().date(),
            'end_date': lambda seq: seq.end_date_time().date(),
            'hour': lambda seq: seq.start_date_time().hour,
            'start_hour': lambda seq: seq.start_date_time().hour,
            'end_hour': lambda seq: seq.end_date_time().hour,
            'day': lambda seq: seq.start_date_time().day,
            'start_day': lambda seq: seq.start_date_time().day,
            'end_day': lambda seq: seq.end_date_time().day,
            'weekday': lambda seq: seq.start_date_time().isoweekday(),
            'start_weekday': lambda seq: seq.start_date_time().isoweekday(),
            'end_weekday': lambda seq: seq.end_date_time().isoweekday()
        }

        # build groupers dict mapping name to grouping function
        groupers = OrderedDict()
        if isinstance(by, FunctionType):
            groupers[by.__name__] = by
        elif isinstance(by, str):
            if by not in lookups.keys():
                raise ValueError('Cannot group by "{}"'.format(by))
            else:
                groupers[by] = lookups[by]
        elif isinstance(by, dict):
            groupers = by
        elif isinstance(by, list):
            for element in by:
                if isinstance(element, str):
                    groupers[element] = lookups[element]
                elif isinstance(element, FunctionType):
                    method_name, num_lambdas = get_method_name(element)
                    groupers[method_name] = element
                else:
                    raise TypeError('List elements must be strings or functions.')

        # calculate dict mapping group-by split names to Sequences
        group_by_names = list(groupers.keys())
        group_bys = OrderedDict([
            (by_name, apply_group_by(groupers[by_name]))
            for by_name in group_by_names
        ])
        result = dict()
        for subgroups_combo in product(*[group_bys[group].items() for group in group_bys.keys()]):
            result_key = tuple([subgroup[0] for subgroup in subgroups_combo])
            result_sequences = [subgroup[1] for subgroup in subgroups_combo]
            result[result_key] = Sequences.intersect_all(result_sequences)
        return SequencesGroupBy(result, names=group_by_names)

    def durations(self):
        """
        :rtype: List[timedelta]
        """
        return [
            sequence.duration() for sequence in self._sequences
        ]

    def map(self, mapper, rtype: type = dict):
        """
        Apply a map function to every Sequence in the Sequences and return the results.

        :param mapper: The method or methods to apply to each UserAction
        :type mapper: Union[str, dict, list, Callable[[IUserAction], Any]]
        :param rtype: Return type of the result: dict or DataFrame
        """
        def map_items(item_mapper):
            if isinstance(item_mapper, str):
                if hasattr(IActionSequence, item_mapper):
                    if callable(getattr(self._sequences[0], item_mapper)):
                        return [getattr(sequence, item_mapper)() for sequence in self._sequences]
                    else:
                        return [getattr(sequence, item_mapper) for sequence in self._sequences]
            elif isinstance(item_mapper, FunctionType):
                return [item_mapper(sequence) for sequence in self._sequences]

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            results = {get_method_name(mapper): map_items(mapper)}
        elif isinstance(mapper, dict):
            results = {
                get_method_name(key): map_items(value)
                for key, value in mapper.items()
            }
        else:
            raise TypeError('mapper must be of type dict, str or function')
        if rtype is dict:
            return results
        elif rtype is DataFrame:
            return DataFrame(results)
        else:
            raise TypeError('rtype must be dict or DataFrame')

    def __getitem__(self, item):

        return self._sequences[item]

    def __repr__(self):

        return 'Sequences({})'.format(len(self._sequences))

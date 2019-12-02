from collections import defaultdict, OrderedDict
from itertools import chain, product
from pandas import concat, DataFrame, Series
from types import FunctionType
from typing import Dict, List

from ux.classes.sequences.sequences_group_by import SequencesGroupBy
from ux.custom_types import SequenceFilter
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences
from ux.utils.misc import get_method_name


class Sequences(ISequences):

    def __init__(self, sequences: List[IActionSequence]):
        """
        Create a new Sequences collection.

        :param sequences: List of ActionSequences to use to create the object.
        """
        self._sequences = sequences

    @property
    def sequences(self):
        """
        Return a list of the individual Sequences in the collection.

        :rtype: List[IActionSequence]
        """
        return self._sequences

    def filter(self, condition: SequenceFilter):
        """
        Return a new Sequences containing only the sequences matching the `condition`.

        :param condition: lambda(sequence) that returns True to include a sequence.
        :rtype: ISequences
        """
        filtered = []
        for sequence in self._sequences:
            if condition(sequence):
                filtered.append(sequence)
        return Sequences(filtered)

    def group_filter(self, filters: Dict[str, SequenceFilter]):
        """
        Return a new SequencesGroupBy keyed by the dict key with values matching each filter, applied in parallel.

        :param filters: Dictionary of filters to apply.
        :rtype: SequencesGroupBy
        """
        filtered = {
            filter_name: self.filter(filter_condition)
            for filter_name, filter_condition in filters.items()
        }
        return SequencesGroupBy(data=filtered, names=['filter'])

    def chain_filter(self, filters: Dict[str, SequenceFilter]):
        """
        Return a new SequencesGroupBy keyed by the dict key with values matching each filter, applied in series.

        :param filters: Dictionary of filters to apply. Use OrderedDict for Python < 3.7 to preserve key order.
        :rtype: SequencesGroupBy
        """
        filtered = OrderedDict()
        sequences = self._sequences
        for filter_name, filter_func in filters.items():
            filtered_sequences = []
            for sequence in sequences:
                if filter_func(sequence):
                    filtered_sequences.append(sequence)
            filtered[filter_name] = Sequences(filtered_sequences)
            sequences = filtered_sequences
        return SequencesGroupBy(data=filtered, names=['filter'])

    def count(self):
        """
        Return the number of ActionSequences in the collection.

        :rtype: int
        """
        return len(self._sequences)

    def copy(self):
        """
        Return a new collection referencing this collection's ActionSequences.

        :rtype: ISequences
        """
        return Sequences(self._sequences)

    def intersection(self, other):
        """
        Return a new collection representing the ActionSequences in both collections.

        :type other: Union[Sequences, List[IActionSequence]]
        :rtype: ISequences
        """
        if type(other) is Sequences:
            other = other.sequences
        return Sequences(
            list(set(self._sequences).intersection(other))
        )

    @staticmethod
    def intersect_all(sequences):
        """
        Return a new collection representing the ActionSequences in every collection.

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
            'end_weekday': lambda seq: seq.end_date_time().isoweekday(),
            'week': lambda seq: seq.start_date_time().isocalendar()[1],
            'start_week': lambda seq: seq.start_date_time().isocalendar()[1],
            'end_week': lambda seq: seq.end_date_time().isocalendar()[1],
            'month': lambda seq: seq.start_date_time().month,
            'start_month': lambda seq: seq.start_date_time().month,
            'end_month': lambda seq: seq.end_date_time().month
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
            if len(result_key) == 1:
                result_key = result_key[0]
            result_sequences = [subgroup[1] for subgroup in subgroups_combo]
            result[result_key] = Sequences.intersect_all(result_sequences)
        return SequencesGroupBy(result, names=group_by_names)

    def durations(self, rtype: type = list):
        """
        :rtype: List[timedelta]
        """
        durations = [
            sequence.duration() for sequence in self._sequences
        ]
        if rtype is list:
            return durations
        elif rtype is Series:
            return Series(
                data=durations,
                name='durations'
            )
        else:
            raise TypeError('rtype must be list or Series')

    def action_template_counts(self, rtype: type = dict):
        """
        Return a total count of all the ActionTemplates in the ActionSequences in the collection.

        :rtype: Dict[IActionTemplate, int]
        """
        total = concat([
            sequence.action_template_counts(Series)
            for sequence in self._sequences
        ], axis=1).sum(axis=1).astype(int)
        if rtype is Series:
            return total
        elif rtype is dict:
            return total.to_dict()
        else:
            raise TypeError('rtype must be dict or Series')

    def action_template_sequence_counts(self, rtype: type = dict):
        """
        Return a total count of the number of ActionSequences containing each ActionTemplate in the collection.

        :rtype: Dict[IActionTemplate, int]
        """
        counts = Series(chain.from_iterable([
            list(sequence.action_template_set()) for sequence in self._sequences
        ])).value_counts()
        if rtype is Series:
            return counts
        elif rtype is dict:
            return counts.to_dict()
        else:
            raise TypeError('rtype must be dict or Series')

    def action_template_transition_counts(self, rtype: type = dict):
        """
        Return counts of transitions between pairs of Actions from each Sequence in the collection.

        :return: Dictionary of {(from, to) => count}
        :rtype: Dict[tuple[IActionTemplate, IActionTemplate], int]
        """
        transitions = defaultdict(int)
        # count transitions
        for sequence in self._sequences:
            for a in range(len(sequence) - 1):
                from_action = sequence.user_actions[a].template()
                to_action = sequence.user_actions[a + 1].template()
                transitions[(from_action, to_action)] += 1
        if rtype is dict:
            return dict(transitions)
        elif rtype is Series:
            transitions = Series(transitions).sort_values(ascending=False)
            transitions.name = 'count'
            transitions.index.name = ['from', 'to']
            return transitions
        else:
            raise TypeError('rtype must be dict or Series')

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

    def __len__(self):

        return len(self._sequences)

    def __contains__(self, item: IActionSequence):

        if isinstance(item, IActionSequence):
            return item in self._sequences
        else:
            raise TypeError('item must be IActionSequence')

    def __iter__(self):

        return self._sequences.__iter__()

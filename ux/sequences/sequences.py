from collections import defaultdict, OrderedDict, Counter
from datetime import timedelta, datetime
from itertools import chain, product
from types import FunctionType
from typing import Counter as CounterType, Tuple, Callable, Any
from typing import Dict, Iterator, List, Optional, overload, Union

from pandas import notnull

from ux.actions.action_template import ActionTemplate, ActionTemplatePair
from ux.compound_types import StrPair
from ux.sequences.action_sequence import ActionSequence, SequenceCounter, \
    SequenceFilter, SequenceFilterSet, SequenceGrouper
from ux.sequences.sequences_group_by import SequencesGroupBy
from ux.utils.misc import get_method_name
from ux.wrappers.map_result import MapResult


class Sequences(object):
    _sequence_lookups = {
        'date': lambda seq: seq.start.date(),
        'start_date': lambda seq: seq.start.date(),
        'end_date': lambda seq: seq.end.date(),
        'date_time': lambda seq: seq.start,
        'start': lambda seq: seq.start,
        'end': lambda seq: seq.end,
        'hour': lambda seq: seq.start.hour,
        'start_hour': lambda seq: seq.start.hour,
        'end_hour': lambda seq: seq.end.hour,
        'day': lambda seq: seq.start.day,
        'start_day': lambda seq: seq.start.day,
        'end_day': lambda seq: seq.end.day,
        'weekday': lambda seq: seq.start.isoweekday(),
        'start_weekday': lambda seq: seq.start.isoweekday(),
        'end_weekday': lambda seq: seq.end.isoweekday(),
        'week': lambda seq: seq.start.isocalendar()[1],
        'start_week': lambda seq: seq.start.isocalendar()[1],
        'end_week': lambda seq: seq.end.isocalendar()[1],
        'month': lambda seq: seq.start.month,
        'start_month': lambda seq: seq.start.month,
        'end_month': lambda seq: seq.end.month
    }

    def __init__(self, sequences: List[ActionSequence]):
        """
        Create a new Sequences collection.

        :param sequences: List of ActionSequences to use to create the object.
        """
        self._sequences: List[ActionSequence] = sequences

    @property
    def sequences(self) -> List[ActionSequence]:
        """
        Return a list of the individual Sequences in the collection.
        """
        return self._sequences

    def filter(self, condition: SequenceFilter) -> 'Sequences':
        """
        Return a new Sequences containing only the sequences matching the
        `condition`.

        :param condition: lambda(sequence) that returns True to include a
        sequence.
        """
        if condition in (None, True):
            return self
        filtered = []
        for sequence in self:
            if condition(sequence):
                filtered.append(sequence)
        return Sequences(filtered)

    def group_filter(self, filters: SequenceFilterSet,
                     group_name: str = 'filter') -> SequencesGroupBy:
        """
        Return a new SequencesGroupBy keyed by the filter name with values
        matching each filter, applied in parallel.

        :param filters: Dictionary of filters to apply.
        :param group_name: Name to identify the filter group.
        """
        filtered = {
            filter_name: self.filter(filter_condition)
            for filter_name, filter_condition in filters.items()
        }
        return SequencesGroupBy(data=filtered, names=[group_name])

    def chain_filter(self, filters: SequenceFilterSet) -> SequencesGroupBy:
        """
        Return a new SequencesGroupBy keyed by the dict key with values matching
        each filter, applied in series.

        :param filters: Dictionary of filters to apply. Use OrderedDict for
        Python < 3.7 to preserve key order.
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

    def group_by(
            self,
            by: Union[SequenceGrouper, Dict[str, SequenceGrouper], str, list]
    ) -> SequencesGroupBy:
        """
        Return a SequencesGroupBy keyed by each value returned by a single
        grouper, or each combination of groupers for a list of groupers.
        Each grouper should be a lambda function that returns a picklable value
        e.g. str.

        :param by: lambda(Sequence) or dict[group_name, lambda(Sequence)] or
                   list[str or lambda(Sequence)].
        """

        def apply_group_by(method: SequenceGrouper) -> Dict[str, 'Sequences']:
            splits = defaultdict(list)
            for sequence in self:
                splits[method(sequence)].append(sequence)
            return {
                group_name: Sequences(group_sequences)
                for group_name, group_sequences in splits.items()
            }

        # build groupers dict mapping name to grouping function
        groupers: Dict[str, SequenceGrouper] = OrderedDict()
        if callable(by):
            groupers[by.__name__] = by
        elif isinstance(by, str):
            if by not in self._sequence_lookups.keys():
                raise ValueError('Cannot group by "{}"'.format(by))
            else:
                groupers[by] = self._sequence_lookups[by]
        elif isinstance(by, dict):
            groupers = by
        elif isinstance(by, list):
            for element in by:
                if isinstance(element, str):
                    if element not in self._sequence_lookups.keys():
                        raise ValueError('Cannot group by "{}"'.format(element))
                    else:
                        groupers[element] = self._sequence_lookups[element]
                elif callable(element):
                    method_name = get_method_name(element)
                    groupers[method_name] = element
                else:
                    raise TypeError(
                        'List elements must be strings or functions.')

        # calculate dict mapping group-by split names to Sequences
        group_by_names = list(groupers.keys())
        group_bys = OrderedDict([
            (by_name, apply_group_by(groupers[by_name]))
            for by_name in group_by_names
        ])
        result = dict()
        for subgroups_combo in product(
                *[group_bys[group].items() for group in group_bys.keys()]):
            result_key = tuple([subgroup[0] for subgroup in subgroups_combo])
            if len(result_key) == 1:
                result_key = result_key[0]
            result_sequences = [subgroup[1] for subgroup in subgroups_combo]
            result[result_key] = Sequences.intersect_all(result_sequences)
        return SequencesGroupBy(result, names=group_by_names)

    def map(self, mapper: Union[str, dict, list, SequenceGrouper]) -> MapResult:
        """
        Apply a map function to every Sequence in the Sequences and return the
        results.

        :param mapper: The method or methods to apply to each ActionSequence
        """

        def map_items(item_mapper: Union[str, FunctionType]) -> list:
            if isinstance(item_mapper, str):
                # properties and methods
                if hasattr(ActionSequence, item_mapper):
                    if callable(getattr(self[0], item_mapper)):
                        # methods
                        return [getattr(sequence, item_mapper)() for sequence in
                                self]
                    else:
                        # properties
                        return [getattr(sequence, item_mapper) for sequence in
                                self]
                elif item_mapper in self._sequence_lookups:
                    return [self._sequence_lookups[item_mapper](sequence) for
                            sequence in self]
                else:
                    raise ValueError(
                        f'ActionSequence has no property'
                        f' or attribute named {item_mapper}'
                    )
            elif isinstance(item_mapper, FunctionType):
                return [item_mapper(sequence) for sequence in self]
            else:
                raise TypeError('item mappers must be FunctionType or str')

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            results = OrderedDict(
                [(get_method_name(mapper), map_items(mapper))])
        elif isinstance(mapper, dict):
            results = OrderedDict([
                (get_method_name(key), map_items(value))
                for key, value in mapper.items()
            ])
        elif isinstance(mapper, list):
            results = OrderedDict([
                (get_method_name(item), map_items(item))
                for item in mapper
            ])
        else:
            raise TypeError('mapper must be dict, list, str or FunctionType')

        return MapResult(results)

    def count(self, condition: Optional[SequenceFilter] = None) -> int:
        """
        Return the number of ActionSequences in the collection.
        """
        if condition is None:
            return len(self)
        return len(self.filter(condition))

    def counter(self, get_value: SequenceCounter) -> CounterType[str]:
        """
        Return a dict of counts of each value returned by get_value(action) for
        each action.

        If get_value returns a list then 1 will be added to the counter value
        for each element key of the list.
        If get_value returns a non-list then the returned item will be used as a
        key and it's value increased by 1.

        :param get_value: method that returns a str or list of strs when called
        on an action.
        """
        counts = Counter()
        for sequence in self:
            sequence_result = get_value(sequence)
            if isinstance(sequence_result, list):
                counts += Counter(sequence_result)
            elif isinstance(sequence_result, str):
                counts[sequence_result] += 1
        return counts

    def copy(self) -> 'Sequences':
        """
        Return a new collection referencing this collection's ActionSequences.
        """
        return Sequences(self._sequences)

    def intersection(
            self, other: Union['Sequences', List[ActionSequence]]
    ) -> 'Sequences':
        """
        Return a new collection representing the ActionSequences in both
        collections.
        """
        if type(other) is Sequences:
            other = other.sequences
        return Sequences(
            list(set(self._sequences).intersection(other))
        )

    @staticmethod
    def intersect_all(sequences: List['Sequences']) -> 'Sequences':
        """
        Return a new collection representing the ActionSequences in every
        collection.
        """
        intersect = sequences[0].copy()
        for s in sequences[1:]:
            intersect = intersect.intersection(s)
        return intersect

    def back_click_rates(self) -> Dict[ActionTemplate, float]:

        rates = {}
        counts = self.action_template_counts()
        for template, count in counts.items():
            forwards = count
            backwards = counts.get(template.reversed(), 0)
            rate = backwards / forwards
            if rate <= 1:
                rates[template] = rate
        return rates

    # region sequence property lists

    @property
    def metas(self) -> List[dict]:

        return [sequence.meta for sequence in self]

    @property
    def starts(self) -> List[datetime]:

        return [sequence.start for sequence in self]

    @property
    def ends(self) -> List[datetime]:

        return [sequence.end for sequence in self]

    @property
    def durations(self) -> List[timedelta]:

        return [sequence.duration for sequence in self]

    @property
    def user_ids(self) -> List[str]:
        return [sequence.user_id for sequence in self.sequences]

    @property
    def session_ids(self) -> List[str]:
        return [sequence.session_id for sequence in self.sequences]

    # end region

    def action_template_counts(self) -> Dict[ActionTemplate, int]:
        """
        Return a total count of all the ActionTemplates in the ActionSequences
        in the collection.
        """
        counts = defaultdict(int)
        for sequence in self:
            for template in sequence.action_templates():
                counts[template] += 1
        return dict(counts)

    def action_template_sequence_counts(self) -> Dict[ActionTemplate, int]:
        """
        Return a total count of the number of ActionSequences containing each
        ActionTemplate in the collection.
        """
        counts = Counter(chain.from_iterable(
            list(sequence.action_template_set()) for sequence in self
        ))
        return dict(counts)

    def action_template_transition_counts(
            self
    ) -> Dict[ActionTemplatePair, int]:
        """
        Return counts of transitions between pairs of Actions from each Sequence
        in the collection.

        :return: Dictionary of {(from, to) => count}
        """
        transitions = defaultdict(int)
        # count transitions
        for sequence in self:
            for a in range(len(sequence) - 1):
                from_action = sequence[a].template()
                to_action = sequence[a + 1].template()
                transitions[(from_action, to_action)] += 1
        return dict(transitions)

    def location_transition_counts(
            self, exclude: Union[str, List[str]] = None
    ) -> CounterType[StrPair]:
        """
        Count the transitions from each location to each other location in
        actions in the given sequences.

        :return: Counter[Tuple[from, to], count]
        """
        transitions = Counter()
        if exclude is not None:
            if isinstance(exclude, str):
                exclude = [exclude]
        else:
            exclude = []
        # count transitions
        for sequence in self:
            for action in sequence:
                source = action.source_id
                target = action.target_id
                if (
                        notnull(target) and
                        source not in exclude and
                        target not in exclude
                ):
                    transitions[(source, target)] += 1
        return transitions

    def dwell_times(
            self, sum_by_location: bool, sum_by_sequence: bool
    ) -> Dict[str, Union[timedelta, List[timedelta]]]:
        """
        Return the amount of time spent by the user at each location.

        :param sum_by_location: Whether to sum the durations of time spent at
                                each location or keep as a list.
        :param sum_by_sequence: Whether to sum the durations of time spent at
                                each location in each sequence or keep as a
                                list.
        """
        if sum_by_sequence:
            dwell_times = defaultdict(timedelta)
            for sequence in self:
                for location, duration in sequence.dwell_times(
                        sum_by_location=True).items():
                    dwell_times[location] += duration
        elif not sum_by_location and not sum_by_sequence:
            dwell_times = defaultdict(list)
            for sequence in self:
                for location, durations in sequence.dwell_times(
                        sum_by_location=False).items():
                    dwell_times[location].extend(durations)
        elif sum_by_location and not sum_by_sequence:
            dwell_times = defaultdict(list)
            for sequence in self:
                for location, duration in sequence.dwell_times(
                        sum_by_location=True).items():
                    dwell_times[location].append(duration)
        else:
            raise ValueError(
                'Invalid arguments for sum_per_location'
                ' and / or sum_per_sequence'
            )

        return dwell_times

    def most_probable_location_sequence(
            self,
            exclude: Union[str, List[str]] = None,
            start_at: str = None,
            allow_repeats: bool = True
    ) -> List[str]:
        """
        Find the most probable location sequence.

        :param exclude: Optional list of names to exclude from the sequence.
        :param start_at: Optional name of start state. Leave as None to use most
                         common state.
        :param allow_repeats: Whether to stop building the sequence at the point
                              where a previous item is found or to use a less
                              likely item instead and carry on building the
                              sequence.
        """
        transitions = self.location_transition_counts(exclude=exclude)
        # find most frequent from point
        if start_at is not None:
            current_name = start_at
        else:
            current_name = transitions.most_common(1)[0][0][0]
        sequence = [current_name]
        # iteratively find most frequent transition point from the current point
        found = True
        while found:
            # remove last added location as a possible target
            if not allow_repeats:
                transitions = {from_to: count for from_to, count in
                               transitions.items()
                               if from_to[1] != current_name}
            # find next location
            froms = [from_to[0] for from_to in transitions.keys()]
            if current_name in froms:
                current_name = Counter({
                    from_to: count for from_to, count in transitions.items()
                    if from_to[0] == current_name
                }).most_common(1)[0][0][1]
                # add if not already in sequence
                if current_name not in sequence:
                    sequence.append(current_name)
                else:
                    found = False
            else:
                found = False
        return sequence

    def sort(self, by: str, ascending: bool = True) -> 'Sequences':

        return Sequences(sequences=sorted(
            self._sequences, key=self._sequence_lookups[by],
            reverse=not ascending
        ))

    @overload
    def __getitem__(self, value: int) -> ActionSequence:
        pass

    @overload
    def __getitem__(self, value: slice) -> List[ActionSequence]:
        pass

    def __getitem__(self, value):

        return self._sequences[value]

    def __repr__(self) -> str:

        return 'Sequences({})'.format(len(self._sequences))

    def __len__(self) -> int:

        return len(self._sequences)

    def __contains__(self, item: ActionSequence) -> bool:

        if isinstance(item, ActionSequence):
            return item in self
        else:
            raise TypeError('item must be ActionSequence')

    def __iter__(self) -> Iterator[ActionSequence]:

        return self._sequences.__iter__()

    def __add__(self, other: 'Sequences') -> 'Sequences':

        if isinstance(other, Sequences):
            other = other.sequences
        return Sequences(
            list(set(self._sequences).union(other))
        ).sort('date_time')

    def __sub__(self, other: 'Sequences') -> 'Sequences':

        if isinstance(other, Sequences):
            other = other.sequences
        return Sequences(list(
            set(self._sequences) - set(self._sequences).intersection(other)
        )).sort('date_time')


SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequencesGrouper = Callable[[Sequences], Any]

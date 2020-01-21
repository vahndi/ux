from collections import OrderedDict
from types import FunctionType
from typing import Dict, List, Union, ItemsView, KeysView, ValuesView, Iterator, Tuple, TYPE_CHECKING

from ux.classes.wrappers.map_result import MapResult
from ux.custom_types.sequence_types import (
    SequenceFilter, SequenceFilterSet, SequenceGrouper, SequencesGrouper, SequencesGroupByKey
)
from ux.utils.misc import get_method_name

if TYPE_CHECKING:
    from ux.sequences.sequences import Sequences


class SequencesGroupBy(object):

    def __init__(self, data: Dict[SequencesGroupByKey, 'Sequences'], names: Union[str, List[str]]):
        """
        :param data: Dictionary mapping keys to Sequences collections
        :param names: Names for the key groups
        """
        self._data: Dict[SequencesGroupByKey, 'Sequences'] = OrderedDict(data)
        if type(names) is str:
            names = [names]
        self._names: List[str] = names

        for attribute in self._data.keys():
            try:
                setattr(self, attribute, self._data[attribute])
            except:
                pass

    def count(self) -> MapResult:

        out_dict = OrderedDict([
            (key, sequences.count())
            for key, sequences in self._data.items()
        ])
        return MapResult(out_dict, key_names=self.names, value_names='count')

    def map(self, mapper: Union[str, dict, list, SequencesGrouper]) -> MapResult:
        """
        Apply a map function to every Sequences in the GroupBy and return the results.

        :param mapper: The method or methods to apply to each Sequences
        """
        def map_items(item_mapper: Union[str, FunctionType]) -> list:
            first_sequences: 'Sequences' = list(self._data.values())[0]
            if isinstance(item_mapper, str):
                # properties and methods
                if hasattr(first_sequences, item_mapper):
                    if callable(getattr(first_sequences, item_mapper)):
                        # methods
                        return [getattr(sequences, item_mapper)() for sequences in self._data.values()]
                    else:
                        # properties
                        return [getattr(sequences, item_mapper) for sequences in self._data.values()]
            elif isinstance(item_mapper, FunctionType):
                return [item_mapper(sequences) for sequences in self._data.values()]
            else:
                raise TypeError('item mappers must be FunctionType or str')

        group_names = list(self._data.keys())

        def new_group(names, method) -> Tuple[str, ...]:
            if isinstance(names, str):
                names = [names]
            elif isinstance(names, tuple):
                names = list(names)
            return tuple(names + [get_method_name(method)])

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            keys = [new_group(names, mapper) for names in group_names]
            values = map_items(mapper)
            results = OrderedDict([(key, value) for key, value in zip(keys, values)])
        elif isinstance(mapper, dict):
            results = OrderedDict()
            for map_key, map_func in mapper.items():
                keys = [new_group(names, map_key) for names in group_names]
                values = map_items(map_func)
                results.update(OrderedDict([
                    (key, value) for key, value in zip(keys, values)
                ]))
        elif isinstance(mapper, list):
            results = OrderedDict()
            for map_item in mapper:
                keys = [new_group(names, map_item) for names in group_names]
                values = map_items(map_item)
                results.update(OrderedDict([
                    (key, value) for key, value in zip(keys, values)
                ]))
        else:
            raise TypeError('mapper must be dict, list, str or FunctionType')

        return MapResult(results, key_names=self.names + ['map'])

    def agg(self, agg_funcs: Dict[str, Union[FunctionType, List[FunctionType]]]) -> MapResult:
        """
        :param agg_funcs: dict mapping attributes to one or more aggregation functions e.g. 'duration': np.median
        :return: Dict[Dict['{{func_name}}({{attr_name}})', agg_result]
        """
        results = OrderedDict()
        # build list of agg_key, agg_func pairs
        agg_pairs: List[Tuple] = []
        for k, v in agg_funcs.items():
            if isinstance(v, FunctionType):
                agg_pairs.append((k, v))
            elif isinstance(v, list):
                for f in v:
                    agg_pairs.append((k, f))
            else:
                raise TypeError('agg_funcs values must be FunctionType or List[FunctionType]')
        agg_attr: str
        for agg_attr, agg_func in agg_pairs:
            agg_func_name = get_method_name(agg_func)
            for group_key, sequences in self.items():
                if type(group_key) is str:
                    group_key = (group_key,)
                first_sequences: 'Sequences' = list(self._data.values())[0]
                if hasattr(first_sequences, agg_attr):
                    if callable(getattr(first_sequences, agg_attr)):
                        values = getattr(sequences, agg_attr)()
                    else:
                        values = getattr(sequences, agg_attr)
                    new_keys = tuple(list(group_key) + [agg_attr, agg_func_name])
                    results[new_keys] = agg_func(values)
        return MapResult(data=results,
                         key_names=self.names + ['attribute', 'agg_method'],
                         value_names='agg_result')

    def filter(self, condition: SequenceFilter) -> 'SequencesGroupBy':
        """
        Return a new Sequences containing only the sequences matching the `condition` in each group.

        :param condition: lambda(sequence) that returns True to include a sequence.
        """
        data = {
            key: value.filter(condition)
            for key, value in self._data.items()
        }
        return SequencesGroupBy(data=data, names=self.names)

    def group_filter(self, filters: SequenceFilterSet, group_name: str = None) -> 'SequencesGroupBy':
        """
        Return a new SequencesGroupBy keyed by the filter name with values matching each filter, applied in parallel.

        :param filters: Dictionary of filters to apply.
        :param group_name: Name to identify the filter group.
        """
        names = self._names.copy()
        if group_name is None:
            i = 2
            while 'filter_' + str(i) in names:
                i += 1
            group_name = 'filter_' + str(i)
        if group_name in names:
            raise ValueError(f'Name "{group_name}" already exists in SequencesGroupBy instance.')
        else:
            names.append(group_name)
        data = {}
        for data_filter_names, data_sequences in self._data.items():
            for filter_name, filter_condition in filters.items():
                if type(data_filter_names) is str:
                    new_filter_names = (data_filter_names, filter_name)
                else:
                    new_filter_names = tuple(list(data_filter_names) + [filter_name])
                data[new_filter_names] = data_sequences.filter(filter_condition)
        return SequencesGroupBy(data=data, names=names)

    def group_by(self, by: Union[SequenceGrouper, Dict[str, SequenceGrouper], str, list]) -> 'SequencesGroupBy':
        """
        Return a new SequencesGroupBy keyed by each value returned by a single grouper,
        or each combination of groupers for a list of groupers.
        Each grouper should be a lambda function that returns a picklable value e.g. str.

        :param by: lambda(Sequence) or dict[group_name, lambda(Sequence)] or list[str or lambda(Sequence)].
        """
        new_results = OrderedDict()
        for group_key, group_sequences in self.items():
            if isinstance(group_key, tuple):
                group_key = list(group_key)
            else:
                group_key = [group_key]
            group_sub_results: SequencesGroupBy = group_sequences.group_by(by)
            for group_sub_key, group_sub_values in group_sub_results.items():
                if isinstance(group_sub_key, tuple):
                    group_sub_key = list(group_sub_key)
                else:
                    group_sub_key = [group_sub_key]
                new_results[tuple(group_key + group_sub_key)] = group_sub_values

        return SequencesGroupBy(data=new_results, names=self.names + group_sub_results.names)

    def items(self) -> ItemsView:

        return self._data.items()

    def keys(self) -> KeysView:

        return self._data.keys()

    def values(self) -> ValuesView:

        return self._data.values()

    @property
    def names(self) -> List[str]:

        return self._names
    
    @names.setter
    def names(self, names: List[str]) -> None:

        self._names = names

    def __getitem__(self, item: Union[str, Tuple[str, ...]]) -> 'Sequences':

        return self._data[item]

    def __repr__(self) -> str:

        return 'SequencesGroupBy({})'.format(self._data.__repr__())

    def __len__(self) -> int:

        return len(self._data)

    def __contains__(self, item) -> bool:

        return item in self._data

    def __iter__(self) -> Iterator[SequencesGroupByKey]:

        return self._data.__iter__()

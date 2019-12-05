from collections import defaultdict, OrderedDict
from pandas import DataFrame, Series, MultiIndex
from types import FunctionType
from typing import Dict, List, Union

from ux.classes.wrappers.map_result import MapResult
from ux.custom_types import SequenceFilter, SequencesGroupByKey, ActionGrouper, SequenceFilterSet, SequencesGrouper
from ux.interfaces.sequences.i_sequences import ISequences
from ux.interfaces.sequences.i_sequences_group_by import ISequencesGroupBy
from ux.utils.misc import get_method_name


class SequencesGroupBy(ISequencesGroupBy):

    def __init__(self, data: Dict[SequencesGroupByKey, ISequences], names: Union[str, List[str]]):
        """
        :param data: Dictionary mapping keys to Sequences collections
        :param names: Names for the key groups
        """
        self._data: Dict[SequencesGroupByKey, ISequences] = OrderedDict(data)
        if type(names) is str:
            names = [names]
        self._names: List[str] = names

    def count(self, rtype: type = dict):

        assert rtype in (dict, Series, DataFrame)
        out_dict = {
            key: sequences.count()
            for key, sequences in self._data.items()
        }
        if rtype is dict:
            return out_dict
        elif rtype is Series:
            s = Series(out_dict).sort_index()
            s.index.names = self._names
            return s
        elif rtype is DataFrame:
            if type(list(self._data.keys())[0]) is str:
                return Series(out_dict, name='count')
            else:
                out_data = DataFrame(
                    data=out_dict.values(),
                    index=MultiIndex.from_tuples(out_dict.keys(), names=self._names)
                ).reset_index().rename(columns={0: 'count'})
                return out_data

    def map(self, mapper: Union[str, dict, list, SequencesGrouper]):
        """
        Apply a map function to every Sequences in the GroupBy and return the results.

        :param mapper: The method or methods to apply to each Sequences
        :rtype: MapResult
        """
        def map_items(item_mapper: Union[str, FunctionType]):
            if isinstance(item_mapper, str):
                # properties and methods
                if hasattr(ISequences, item_mapper):
                    if callable(getattr(ISequences, item_mapper)):
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

        def new_group(names, method):
            if isinstance(names, str):
                names = [names]
            return tuple(names + [get_method_name(method)])

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            self._names.append(get_method_name(mapper))
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

        return MapResult(results)

    def agg(self, agg_funcs: dict, rtype: type = dict):
        """
        :param agg_funcs: dict mapping attributes to one or more aggregation functions e.g. duration -> np.median
        :param rtype: Return type of the result: dict or DataFrame
        """
        results = defaultdict(dict)

        # build list of agg_key, agg_func pairs
        agg_pairs = []
        for k, v in agg_funcs.items():
            if isinstance(v, FunctionType):
                agg_pairs.append((k, v))
            else:
                for f in v:
                    agg_pairs.append((k, f))
        for agg_key, agg_func in agg_pairs:
            agg_name = get_method_name(agg_func)
            for name, sequences in self.items():
                if hasattr(ISequences, agg_key):
                    if callable(getattr(ISequences, agg_key)):
                        values = getattr(sequences, agg_key)()
                    else:
                        values = getattr(sequences, agg_key)
                    results[name]['{}({})'.format(agg_name, agg_key)] = agg_func(values)
        if rtype is dict:
            return results
        elif rtype is DataFrame:
            data = DataFrame(results).T.sort_index()
            data.index.names = self._names
            return data
        else:
            raise TypeError('rtype must be dict or DataFrame')

    def filter(self, condition: SequenceFilter):
        """
        Return a new Sequences containing only the sequences matching the `condition` in each group.

        :param condition: lambda(sequence) that returns True to include a sequence.
        :rtype: ISequencesGroupBy
        """
        data = {
            key: value.filter(condition)
            for key, value in self._data.items()
        }
        return SequencesGroupBy(data=data, names=self.names)

    def group_filter(self, filters: SequenceFilterSet, group_name: str = None):
        """
        Return a new SequencesGroupBy keyed by the filter name with values matching each filter, applied in parallel.

        :param filters: Dictionary of filters to apply.
        :param group_name: Name to identify the filter group.
        :rtype: SequencesGroupBy
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

    def items(self):
        """
        :rtype: dict_items
        """
        return self._data.items()

    def keys(self):
        """
        :rtype: dict_keys
        """
        return self._data.keys()

    def values(self):
        """
        :rtype: dict_values
        """
        return self._data.values()

    @property
    def names(self):
        """
        :rtype: List[str]
        """
        return self._names
    
    @names.setter
    def names(self, names):

        self._names = names

    def __getitem__(self, item):
        """
        :rtype: ISequences
        """
        return self._data[item]

    def __repr__(self):

        return 'SequencesGroupBy({})'.format(self._names)

    def __len__(self):

        return len(self._data)

    def __contains__(self, item):

        return item in self._data

    def __iter__(self):

        return self._data.__iter__()

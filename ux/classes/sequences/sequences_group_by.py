from collections import defaultdict

from pandas import DataFrame, Series, MultiIndex
from types import FunctionType
from typing import List

from ux.custom_types import SequenceFilter
from ux.interfaces.sequences.i_sequences import ISequences
from ux.interfaces.sequences.i_sequences_group_by import ISequencesGroupBy
from ux.utils.misc import get_method_name


class SequencesGroupBy(ISequencesGroupBy):

    def __init__(self, data: dict, names: List[str] = None):

        self._data = data
        if type(names) is str:
            names = [names]
        self._names = names

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

    def map(self, mapper):
        """
        Apply a map function to every Sequences in the GroupBy and return the results.

        :param mapper: The method or methods to apply to each UserAction
        :type mapper: Union[str, dict, list, Callable[[IUserAction], Any]]
        :rtype: dict
        """
        def map_items(item_mapper):
            if isinstance(item_mapper, str):
                if hasattr(ISequences, item_mapper):
                    if callable(getattr(ISequences, item_mapper)):
                        return {
                            name: getattr(sequences, item_mapper)()
                            for name, sequences in self.items()
                        }
                    else:
                        return {
                            name: getattr(sequences, item_mapper)
                            for name, sequences in self.items()
                        }
            elif isinstance(item_mapper, FunctionType):
                return {
                    name: item_mapper(sequences)
                    for name, sequences in self.items()
                }

        if isinstance(mapper, str) or isinstance(mapper, FunctionType):
            results = {get_method_name(mapper): map_items(mapper)}
        elif isinstance(mapper, dict):
            results = {
                get_method_name(key): map_items(value)
                for key, value in mapper.items()
            }
        else:
            raise TypeError('mapper must be of type dict, str or function')
        return results

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

    def items(self):

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

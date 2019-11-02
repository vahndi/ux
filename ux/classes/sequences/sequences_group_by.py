from ux.interfaces.sequences.i_sequences import ISequences
from typing import List

from pandas import DataFrame, Series, MultiIndex

from ux.interfaces.sequences.i_sequences_group_by import ISequencesGroupBy


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

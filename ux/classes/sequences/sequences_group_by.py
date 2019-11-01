from typing import List

from pandas import DataFrame, Series, MultiIndex


class SequencesGroupBy(object):

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
            return Series(out_dict)
        elif rtype is DataFrame:
            if type(self._data.keys()[0]) is str:
                return Series(out_dict)
            else:
                out_data = Series(data=out_dict.values(),
                                  index=MultiIndex.from_tuples(out_dict.keys(), names=self._names),
                                  name='count').reset_index()
                return out_data

    def items(self):

        return self._data.items()

    @property
    def names(self):
        return self._names
    
    @names.setter
    def names(self, names):

        self._names = names

    def __repr__(self):

        return 'SequencesGroupBy({})'.format(self._names)

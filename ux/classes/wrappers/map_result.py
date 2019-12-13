from pandas import DataFrame, Series, MultiIndex, Index, concat
from typing import List, Union, Iterable


def _str_or_non_iterable(val):

    return not isinstance(val, Iterable) or isinstance(val, str)


class MapResult(object):

    def __init__(self, data: dict,
                 key_names: Union[str, List[str]] = 'map',
                 value_names: Union[str, List[str]] = 'result'):

        if isinstance(key_names, str):
            key_names = [key_names]
        if isinstance(value_names, str):
            value_names = [value_names]

        # check key names
        if all(_str_or_non_iterable(k) for k in list(data.keys())):
            assert len(key_names) == 1, 'Length of index names must be 1 when keys are not Iterables'
        else:
            assert len(key_names) == len(list(data.keys())[0]), 'Keys must have same length as index_names'

        # check value names
        assert len(value_names) == 1, 'value_names must be length 1'

        self._data: dict = data
        self._index_names = key_names
        self._data_names = value_names

        self._first_key = list(data.keys())[0]
        self._first_value = list(data.values())[0]

        for attribute in self._data.keys():
            try:
                setattr(self, attribute, self._data[attribute])
            except:
                pass

    @property
    def index_names(self):
        return self._index_names

    @property
    def data_names(self):
        return self._data_names

    def to_series(self):
        """
        :rtype: Series
        """
        if _str_or_non_iterable(self._first_key):
            if _str_or_non_iterable(self._first_value):
                # e.g. {'a': 1, 'b': 2, 'c': 3}
                series = Series(self._data, name=self.data_names[0])
                series.index.name = self.index_names[0]
            else:
                # e.g. {'a': [1, 2], 'b': [3, 4, 5]}
                series = concat([
                    Series(
                        index=Index([key] * len(values), name=self.index_names[0]),
                        data=values, name=self.data_names[0]
                    )
                    for key, values in self._data.items()
                ])
        else:
            if _str_or_non_iterable(self._first_value):
                # e.g. {('a', 'b'): 1, ('c', 'd'): 2, ('e', 'f'): 3}
                series = Series(self._data, name=self.data_names[0])
                series.index.names = self.index_names
            else:
                # e.g. {('a', 'b'): [1, 2], ('c', 'd'): [3, 4, 5]}
                series = concat([
                    Series(
                        index=MultiIndex.from_tuples([key] * len(values), names=self.index_names),
                        data=values, name=self.data_names[0]
                    )
                    for key, values in self._data.items()
                ])

        return series

    def to_dict(self):
        """
        :rtype: dict
        """
        return self._data

    def to_frame(self, wide: bool = False):
        """
        :rtype: DataFrame
        """
        if not wide:
            return self.to_series().to_frame().reset_index()
        else:
            try:
                return DataFrame(self._data)
            except:
                return self.to_series().to_frame().reset_index()

    def to_list(self):
        """
        :rtype: list
        """
        return list(self.to_series().tolist())

    def to_tuples(self):
        """
        :rtype: List[tuple]
        """
        return list(self.to_frame().to_records())

    def items(self):

        return self._data.items()

    def keys(self):

        return self._data.keys()

    def values(self):

        return self._data.values()

    def __getitem__(self, item):

        return self._data[item]

    def __iter__(self):

        return self._data.__iter__()

    def __repr__(self):

        return 'MapResult({})'.format(self._data.__repr__())

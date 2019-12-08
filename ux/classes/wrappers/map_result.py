from typing import List

from pandas import DataFrame, Series, MultiIndex, Index


class MapResult(object):

    def __init__(self, data: dict, index_names: List[str] = None, data_names: List[str] = None):

        self._data: dict = data
        self._index_names = index_names
        self._data_names = data_names

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

    def to_list(self):
        """
        :rtype: list
        """
        if len(self.keys()) != 1:
            raise ValueError('Can only output a list for a single-dimensional map result')
        return list(self._data.values())[0]

    def _pandas_index(self):

        if isinstance(list(self.keys())[0], tuple):
            return MultiIndex.from_tuples(self.keys(), names=self._index_names)
        else:
            return Index(self.keys(), name=self._index_names[0])

    def to_series(self):
        """
        :rtype: Series
        """
        if len(self.keys()) != 1:
            return Series(
                index=self._pandas_index(),
                data=list(self.values()),
                name=self._data_names[0]
            )
        else:
            return Series(
                data=list(self._data.values())[0],
                name=list(self._data.keys())[0]
            )

    def to_dict(self):
        """
        :rtype: dict
        """
        return self._data

    def to_frame(self):
        """
        :rtype: DataFrame
        """
        if not isinstance(list(self.values())[0], list):
            return self.to_series().to_frame()
        else:
            return DataFrame(self._data)

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

from pandas import DataFrame, Series


class MapResult(object):

    def __init__(self, data: dict):

        self._data: dict = data

    def to_list(self):
        """
        :rtype: list
        """
        if len(self.keys()) != 1:
            raise ValueError('Can only output a list for a single-dimensional map result')
        return list(self._data.values())[0]

    def to_series(self):
        """
        :rtype: Series
        """
        if len(self.keys()) != 1:
            raise ValueError('Can only output a Series for a single-dimensional map result')
        return Series(data=list(self._data.values())[0],
                      name=list(self._data.keys())[0])

    def to_dict(self):
        """
        :rtype: dict
        """
        return self._data

    def to_frame(self):
        """
        :rtype: DataFrame
        """
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

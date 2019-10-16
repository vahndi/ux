from pandas import Series, DataFrame, MultiIndex


class TemporalCount(dict):

    def __init__(self, name: str):
        """
        Create a new Temporal Count representing the count of a single or split variable over time.

        :param name: The name of the metric or measure being counted.
        """
        super(TemporalCount, self).__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_split(self):
        """
        :rtype: bool
        """
        return type(list(self.values())[0]) is dict

    def to_series(self):
        """
        Return the Series representation of the count data.

        If the count is split, return counts indexed by datetime and count variable.
        If the count is not split return counts indexed by datetime.

        :rtype: Series
        """
        if self.is_split:
            data = DataFrame(self).T
            data.index.name = 'date_time'
            data = data.reset_index().melt(
                id_vars='date_time', var_name=self._name, value_name='count'
            )
            data = data.set_index(['date_time', self._name])['count']
            return data
        else:
            data = Series(data=self, name=self._name)
            data.index.name = 'date_time'
            return data

    def to_frame(self):
        """
        Return the DataFrame representation of the count data.

        If the count is split then each split key will be represented by a 2-level column.
        If the count is not split then there will be one column, named after the TemporalCount.
        In either case the Index will be the datetime of the count.

        :rtype: DataFrame
        """
        if self.is_split:
            data = DataFrame(self).T
            data.index.name = 'date_time'
            data.columns = MultiIndex.from_product([[self._name], data.columns])
            return data
        else:
            return self.to_series().to_frame()

    def to_pandas(self):
        """
        Return the most natural representation of the count as a pandas object.

        :return: Pandas DataFrame if the count is split otherwise a Series.
        """
        if self.is_split:
            return self.to_frame()
        else:
            return self.to_series()

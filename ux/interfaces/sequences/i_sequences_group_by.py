class ISequencesGroupBy(object):

    def count(self, rtype: type = dict):

        raise NotImplementedError

    def items(self):

        raise NotImplementedError

    def keys(self):
        """
        :rtype: dict_keys
        """
        raise NotImplementedError

    def values(self):
        """
        :rtype: dict_values
        """
        raise NotImplementedError

    @property
    def names(self):
        """
        :rtype: List[str]
        """
        raise NotImplementedError

    def map(self, mapper):

        raise NotImplementedError

    def agg(self, agg_funcs: dict, rtype: type = dict):
        """
        :param agg_funcs: dict mapping attributes to one or more aggregation functions e.g. duration -> np.median
        :param rtype: Return type of the result: dict or DataFrame
        """
        raise NotImplementedError

    def __getitem__(self, item):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

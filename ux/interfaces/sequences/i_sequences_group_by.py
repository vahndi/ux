class ISequencesGroupBy(object):

    def count(self):

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

    def agg(self, agg_funcs: dict):
        """
        :param agg_funcs: dict mapping attributes to one or more aggregation functions e.g. duration -> np.median
        """
        raise NotImplementedError

    def filter(self, condition):
        """
        Return a new Sequences containing only the sequences matching the `condition` in each group.

        :param condition: lambda(sequence) that returns True to include a sequence.
        :rtype: ISequencesGroupBy
        """
        raise NotImplementedError

    def group_filter(self, filters, group_name=None):
        """
        Return a new SequencesGroupBy keyed by the filter name with values matching each filter, applied in parallel.

        :param filters: Dictionary of filters to apply.
        :param group_name: Name to identify the filter group.
        :rtype: SequencesGroupBy
        """
        raise NotImplementedError

    def __getitem__(self, item):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

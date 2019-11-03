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

    def __getitem__(self, item):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

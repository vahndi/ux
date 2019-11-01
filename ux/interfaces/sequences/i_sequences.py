class ISequences(object):

    @property
    def sequences(self):
        raise NotImplementedError

    def filter(self, condition: callable):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def count(self):
        """
        :rtype: int
        """
        raise NotImplementedError

    def copy(self):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

    def intersection(self, other):
        """
        :rtype: ISequences
        """
        raise NotImplementedError

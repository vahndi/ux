class IActionTemplate(object):

    @property
    def action_type(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def source_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def target_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def weighting(self):
        """
        :rtype: float
        """
        raise NotImplementedError

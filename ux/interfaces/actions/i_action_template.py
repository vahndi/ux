class IActionTemplate(object):

    @property
    def action_type(self):
        """
        Return the type of the ActionTemplate.

        :rtype: str
        """
        raise NotImplementedError

    @property
    def source_id(self):
        """
        Return the id of the Location where the Action would be taken.

        :rtype: str
        """
        raise NotImplementedError

    @property
    def target_id(self):
        """
        Return the id of the Location where the Action would go to.

        :rtype: str
        """
        raise NotImplementedError

    @property
    def weighting(self):
        """
        Return the weighting for the Action for various calculations.

        :rtype: float
        """
        raise NotImplementedError

    def reversed(self, action_type: str = None):
        """
        Return a reversed version of the template (switch the source and target).

        :param action_type: Optional action type. Leave as None to use the existing action type.
        :rtype: IActionTemplate
        """
        raise NotImplementedError

    def to_dict(self):
        """
        :rtype: dict
        """
        raise NotImplementedError

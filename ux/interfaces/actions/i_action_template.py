class IActionTemplate(object):

    @property
    def action_type(self) -> str:
        """
        Return the type of the ActionTemplate.
        """
        raise NotImplementedError

    @property
    def source_id(self) -> str:
        """
        Return the id of the Location where the Action would be taken.
        """
        raise NotImplementedError

    @property
    def target_id(self) -> str:
        """
        Return the id of the Location where the Action would go to.
        """
        raise NotImplementedError

    @property
    def weighting(self) -> float:
        """
        Return the weighting for the Action for various calculations.
        """
        raise NotImplementedError

    def reversed(self, action_type: str = None) -> 'IActionTemplate':
        """
        Return a reversed version of the template (switch the source and target).

        :param action_type: Optional action type. Leave as None to use the existing action type.
        """
        raise NotImplementedError

    def to_dict(self) -> dict:

        raise NotImplementedError

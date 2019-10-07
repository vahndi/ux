from ux.interfaces.actions.i_action_template import IActionTemplate


class ActionTemplate(IActionTemplate):
    """
    Represents a Template for a single Action that could be taken by a User.
    """
    def __init__(self, action_type: str, source_id: str, target_id: str = None,
                 weighting: float = 1):
        """
        Create a new ActionTemplate.

        :param action_type: A type for the Action (used in matching)
        :param source_id: The id of the Location where the Action would be taken (used in matching).
        :param target_id: Optional id of the Location where the Action would go to (used in matching).
        :param weighting: Optional weighting value to use in various calculations.
        """
        self._action_type = action_type
        self._source_id = source_id
        self._target_id = target_id
        self._weighting = weighting

    @property
    def action_type(self):
        """
        Return the type of the ActionTemplate.

        :rtype: str
        """
        return self._action_type

    @property
    def source_id(self):
        """
        Return the id of the Location where the Action would be taken.

        :rtype: str
        """
        return self._source_id

    @property
    def target_id(self):
        """
        Return the id of the Location where the Action would go to.

        :rtype: str
        """
        return self._target_id

    @property
    def weighting(self):
        """
        Return the weighting for the Action for various calculations.

        :rtype: float
        """
        return self._weighting

    def __eq__(self, other):
        """
        :type other: ActionTemplate
        """
        return (
            (self._action_type == other._action_type or '*' in (self._action_type, other._action_type)) and
            (self._source_id == other._source_id or '*' in (self._source_id, other._source_id)) and
            (self._target_id == other._target_id or '*' in (self._target_id, other._target_id))
        )

    def __repr__(self):

        return 'ActionTemplate({}: {}{}{})'.format(
            self._action_type, self._source_id,
            ' → ' if self._target_id else '',
            self._target_id if self._target_id else ''
        )

    def to_dict(self):

        return {
            'action_type': self._action_type,
            'source_id': self._source_id,
            'target_id': self._target_id
        }

    def __hash__(self):

        return hash(tuple(sorted(self.to_dict().items())))

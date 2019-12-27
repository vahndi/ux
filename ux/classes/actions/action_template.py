from typing import Optional

from ux.interfaces.actions.i_action_template import IActionTemplate


class ActionTemplate(IActionTemplate):
    """
    Represents a Template for a single Action that could be taken by a User.
    """
    def __init__(self, action_type: str, source_id: str, target_id: Optional[str] = None,
                 weighting: float = 1):
        """
        Create a new ActionTemplate.

        :param action_type: A type for the Action (used in matching)
        :param source_id: The id of the Location where the Action would be taken (used in matching).
        :param target_id: Optional id of the Location where the Action would go to (used in matching).
        :param weighting: Optional weighting value to use in various calculations.
        """
        self._action_type: str = action_type
        self._source_id: str = source_id
        self._target_id: Optional[str] = target_id
        self._weighting: float = weighting

    @property
    def action_type(self) -> str:
        """
        Return the type of the ActionTemplate.
        """
        return self._action_type

    @property
    def source_id(self) -> str:
        """
        Return the id of the Location where the Action would be taken.
        """
        return self._source_id

    @property
    def target_id(self) -> Optional[str]:
        """
        Return the id of the Location where the Action would go to.
        """
        return self._target_id

    @property
    def weighting(self) -> float:
        """
        Return the weighting for the Action for various calculations.
        """
        return self._weighting

    def reversed(self, action_type: str = None) -> IActionTemplate:
        """
        Return a reversed version of the template (switch the source and target).

        :param action_type: Optional action type. Leave as None to use the existing action type.
        """
        return ActionTemplate(
            source_id=self.target_id,
            target_id=self.source_id,
            action_type=action_type or self.action_type
        )

    def to_dict(self) -> dict:

        return {
            'action_type': self._action_type,
            'source_id': self._source_id,
            'target_id': self._target_id
        }

    def __eq__(self, other) -> bool:
        """
        :type other: ActionTemplate
        """
        return (
            (self._action_type == other._action_type or '*' in (self._action_type, other._action_type)) and
            (self._source_id == other._source_id or '*' in (self._source_id, other._source_id)) and
            (self._target_id == other._target_id or '*' in (self._target_id, other._target_id))
        )

    def __repr__(self) -> str:

        return 'ActionTemplate({}: {}{}{})'.format(
            self._action_type, self._source_id,
            ' → ' if self._target_id else '',
            self._target_id if self._target_id else ''
        )

    def __hash__(self):

        return hash(tuple(sorted(self.to_dict().items())))

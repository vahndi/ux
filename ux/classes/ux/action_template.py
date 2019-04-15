from ux.interfaces.ux.i_action_template import IActionTemplate


class ActionTemplate(IActionTemplate):

    def __init__(self, action_type: str, source_id: str, target_id: str = None):

        self._action_type = action_type
        self._source_id = source_id
        self._target_id = target_id

    @property
    def action_type(self):
        return self._action_type

    @property
    def source_id(self):
        return self._source_id

    @property
    def target_id(self):
        return self._target_id

    def __eq__(self, other):
        """
        :type other: ActionTemplate
        """
        return (
            self.action_type == other._action_type and
            self.source_id == other._source_id and
            self.target_id == other._target_id
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

from typing import List

from ux.interfaces.actions.i_action_template import IActionTemplate


class ITask(object):

    @property
    def name(self) -> str:

        raise NotImplementedError

    @property
    def action_templates(self) -> List[IActionTemplate]:

        raise NotImplementedError

    def unordered_completion_rate(self, action_sequence) -> float:
        """
        :type action_sequence: IActionSequence
        """
        raise NotImplementedError

    def ordered_completion_rate(self, action_sequence) -> float:
        """
        :type action_sequence: IActionSequence
        """
        raise NotImplementedError

    def intersects_sequence(self, action_sequence) -> bool:
        """
        :type action_sequence: IActionSequence
        """
        raise NotImplementedError

    def __getitem__(self, item) -> IActionTemplate:

        raise NotImplementedError

    def __len__(self) -> int:

        raise NotImplementedError

    def __contains__(self, item) -> bool:

        raise NotImplementedError

    def __iter__(self) -> IActionTemplate:

        raise NotImplementedError

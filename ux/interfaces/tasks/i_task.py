from typing import List, Optional

from ux.interfaces.actions.i_action_template import IActionTemplate


class ITask(object):

    @property
    def name(self) -> str:

        raise NotImplementedError

    @property
    def action_templates(self) -> List[IActionTemplate]:

        raise NotImplementedError

    # region action template property lists

    @property
    def source_ids(self) -> List[str]:
        raise NotImplementedError

    @property
    def target_ids(self) -> List[Optional[str]]:
        raise NotImplementedError

    @property
    def action_types(self) -> List[str]:
        raise NotImplementedError

    @property
    def weightings(self) -> List[float]:
        raise NotImplementedError

    # end region

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

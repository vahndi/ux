from typing import Callable, Dict, Optional

from ux.classes.actions.user_action import UserAction
from ux.classes.sequences.action_sequence import ActionSequence
from ux.custom_types.action_types import ActionFilter
from ux.custom_types.sequence_types import SequenceFilter


class CountConfig(object):

    def __init__(self, name: str,
                 sequence_condition: Optional[SequenceFilter] = None,
                 sequence_split_by: Optional[Callable[[ActionSequence], Dict[str, int]]] = None,
                 action_condition: Optional[ActionFilter] = None,
                 action_split_by: Optional[Callable[[UserAction], Dict[str, int]]] = None):
        """
        Configuration class for batch calculation of count metrics.

        - If counting sequences, must pass `sequence_condition` and `sequence_split_by`.
        - If counting actions within sequences, must also pass `action_condition` and `action_split_by`
        - set `sequence_condition` or `action_condition` to `lambda x: True` to include all sequences or actions

        :param name: Name of the count metric.
        :param sequence_condition: lambda(sequence) that must return True for a sequence to be included in the count.
        :param sequence_split_by:  lambda(sequence) that splits sequence counts into dict[split_name, count]
        :param action_condition: lambda(action) that must return True for an action to be included in the count.
        :param action_split_by: lambda(action) that splits action counts into dict[split_name, count]
        """
        if action_condition is not None:
            assert sequence_condition is not None
        self.name: str = name
        self.sequence_condition: Optional[SequenceFilter] = sequence_condition
        self.sequence_split_by: Optional[Callable[[ActionSequence], Dict[str, int]]] = sequence_split_by
        self.action_condition: Optional[ActionFilter] = action_condition
        self.action_split_by: Optional[Callable[[UserAction], Dict[str, int]]] = action_split_by

    def __repr__(self) -> str:

        args = ['name', 'sequence_condition', 'sequence_split_by', 'action_condition', 'action_split_by']
        return 'CountConfig({})'.format(', '.join(['{}={}'.format(arg, getattr(self, arg)) for arg in args]))

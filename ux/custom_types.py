from typing import Callable, Dict, Tuple, Union, Any

from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.sequences.i_action_sequence import IActionSequence


ActionFilter = Callable[[IUserAction], bool]
ActionGrouper = Callable[[IUserAction], Any]
SequenceFilter = Callable[[IActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]
SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequenceGrouper = Callable[[IActionSequence], Any]

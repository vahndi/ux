from typing import Callable, Dict, Tuple, Union, Any, Iterable

from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences


ActionFilter = Callable[[IUserAction], bool]
ActionMapper = Callable[[IUserAction], Any]
SequenceFilter = Callable[[IActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]
SequenceGrouper = Callable[[IActionSequence], Any]
SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequencesGrouper = Callable[[ISequences], Any]

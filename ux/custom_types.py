from typing import Any, Callable, Dict, Tuple, Union, List

from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences


ActionCounter = Callable[[IUserAction], Union[str, List[str]]]
ActionFilter = Callable[[IUserAction], bool]
ActionMapper = Callable[[IUserAction], Any]
ActionGrouper = Callable[[IUserAction], Any]

SequenceCounter = Callable[[IActionSequence], Union[str, List[str]]]
SequenceFilter = Callable[[IActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]
SequenceGrouper = Callable[[IActionSequence], Any]

SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequencesGrouper = Callable[[ISequences], Any]

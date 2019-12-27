from typing import Callable, Union, List, Dict, Any, Tuple

from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences import ISequences
from ux.interfaces.tasks.i_task import ITask

SequenceCounter = Callable[[IActionSequence], Union[str, List[str]]]
SequenceFilter = Callable[[IActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]
SequenceGrouper = Callable[[IActionSequence], Any]
SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequencesGrouper = Callable[[ISequences], Any]

TaskPair = Tuple[ITask, ITask]

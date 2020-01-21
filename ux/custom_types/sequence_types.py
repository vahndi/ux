from typing import Callable, Union, List, Dict, Any, Tuple

from ux.classes.sequences.action_sequence import ActionSequence
from ux.classes.sequences.sequences import Sequences
from ux.classes.tasks.task import Task


SequenceCounter = Callable[[ActionSequence], Union[str, List[str]]]
SequenceFilter = Callable[[ActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]
SequenceGrouper = Callable[[ActionSequence], Any]
SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequencesGrouper = Callable[[Sequences], Any]

TaskPair = Tuple[Task, Task]

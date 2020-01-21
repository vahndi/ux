from typing import Callable, Union, List, Dict, Any, Tuple

from ux.sequences import ActionSequence
from ux.sequences.sequences import Sequences
from ux.tasks import Task


SequenceCounter = Callable[[ActionSequence], Union[str, List[str]]]
SequenceFilter = Callable[[ActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]
SequenceGrouper = Callable[[ActionSequence], Any]
SequencesGroupByKey = Union[str, Tuple[str, ...]]
SequencesGrouper = Callable[[Sequences], Any]

TaskPair = Tuple[Task, Task]

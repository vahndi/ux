from typing import Callable, Dict

from ux.interfaces.actions.i_user_action import IUserAction
from ux.interfaces.sequences.i_action_sequence import IActionSequence


ActionFilter = Callable[[IUserAction], bool]
SequenceFilter = Callable[[IActionSequence], bool]
SequenceFilterSet = Dict[str, SequenceFilter]

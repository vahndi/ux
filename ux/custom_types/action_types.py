from typing import Callable, Union, List, Any, Tuple

from ux.classes.actions.action_template import ActionTemplate
from ux.classes.actions.user_action import UserAction


ActionCounter = Callable[[UserAction], Union[str, List[str]]]
ActionFilter = Callable[[UserAction], bool]
ActionMapper = Callable[[UserAction], Any]
ActionGrouper = Callable[[UserAction], Any]
ActionTemplatePair = Tuple[ActionTemplate, ActionTemplate]

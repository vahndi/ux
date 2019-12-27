from typing import Callable, Union, List, Any, Tuple

from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.actions.i_user_action import IUserAction

ActionCounter = Callable[[IUserAction], Union[str, List[str]]]
ActionFilter = Callable[[IUserAction], bool]
ActionMapper = Callable[[IUserAction], Any]
ActionGrouper = Callable[[IUserAction], Any]
ActionTemplatePair = Tuple[IActionTemplate, IActionTemplate]

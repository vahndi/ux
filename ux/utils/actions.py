from types import FunctionType
from typing import Union

from ux.interfaces.actions.i_action_template import IActionTemplate


def create_action_template_condition(value):
    """
    :type value: Union[IActionTemplate, FunctionType]
    :rtype: FunctionType
    """
    def action_template_condition(template: IActionTemplate):
        if template == value:
            return True
        else:
            return False

    if isinstance(value, IActionTemplate):
        return action_template_condition
    elif isinstance(value, FunctionType):
        return value
    else:
        raise TypeError('expected IActionTemplate or FunctionType')

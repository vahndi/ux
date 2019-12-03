from types import FunctionType
from typing import Union


def get_method_name(method: Union[str, FunctionType]):
    """
    :rtype: str
    """
    if isinstance(method, str):
        return method
    elif isinstance(method, FunctionType):
        name = method.__name__
        if name != '<lambda>':
            return name
        else:
            return str(method)

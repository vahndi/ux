from re import compile
from types import FunctionType
from typing import Union

function_exp = compile(r'<function (\w+) at \w+>')


def get_method_name(method: Union[str, FunctionType]) -> str:

    if isinstance(method, str):
        return method
    elif isinstance(method, FunctionType):
        name = method.__name__
        if name != '<lambda>':
            return name
        elif function_exp.match(str(method)):
            return function_exp.match(str(method)).groups()[0]
        else:
            return str(method)

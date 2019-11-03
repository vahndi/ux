from types import FunctionType


def get_method_name(method):

    if isinstance(method, str):
        return method
    elif isinstance(method, FunctionType):
        name = method.__name__
        if name != '<lambda>':
            return name
        else:
            return str(method)

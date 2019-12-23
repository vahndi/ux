def page_view(source: str, target: str) -> str:
    """
    Return every action as a "page-view" action type.

    :param source: Name of the source location.
    :param target: Name of the target location, if any.
    """
    return 'page-view'


def page_view__back_click(source: str, target: str) -> str:
    """
    Return forward actions as "page-view"s and backwards actions as "back-click" action type.

    :param source: Name of the source location.
    :param target: Name of the target location, if any.
    """
    if target > source:
        return 'page-view'
    elif source > target:
        return 'back-click'
    else:
        raise ValueError('source cannot equal target')

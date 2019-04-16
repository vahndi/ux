from math import sqrt


def lostness(unique: int, total: int, optimum: int):
    """
    Calculate the `lostness` metric for the given pages.

    :param total: The total number of locations visited while performing the task, counting revisits to the same page.
    :param unique: The number of different locations visited while performing the task.
    :param optimum: The minimum (optimum) number of locations that must be visited to accomplish the task.
    :rtype: float
    """
    return sqrt(
        (unique / total - 1) ** 2 +
        (optimum / unique - 1) ** 2
    )

from math import cos, sin, radians
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import List, Union

from ux.interfaces.ux.i_location import ILocation


def new_axes():
    """
    :rtype: Axes
    """
    _, ax = plt.subplots()
    return ax


def get_hist_index(bin_values: List[int]):
    """
    Return index labels for histogram bin values.

    :rtype:  List[str]
    """
    return [
        '{}%-{}%'.format(bin_values[b], bin_values[b + 1])
        for b in range(len(bin_values) - 1)
    ]


def point_distance(point_1: tuple, point_2: tuple):
    """
    Calculate the distance from point_1 to point_2.

    :rtype: float
    """
    return (
        (point_1[0] - point_2[0]) ** 2 +
        (point_1[1] - point_2[1]) ** 2
    ) ** 0.5


def circle_edge(point_1: tuple, point_2: tuple, radius: float, rotation_angle: float = 0.0):
    """
    Calculate the closest point on the edge of a circle centered at point_1 with radius to point_2.

    :rtype: tuple
    """
    distance = point_distance(point_1, point_2)
    edge_point = (
        point_1[0] + radius * (point_2[0] - point_1[0]) / distance,
        point_1[1] + radius * (point_2[1] - point_1[1]) / distance
    )
    if rotation_angle != 0:
        rotation_angle = radians(rotation_angle)
        ox, oy = point_1
        px, py = edge_point
        qx = ox + cos(rotation_angle) * (px - ox) - sin(rotation_angle) * (py - oy)
        qy = oy + sin(rotation_angle) * (px - ox) + cos(rotation_angle) * (py - oy)
        edge_point = qx, qy

    return edge_point


def get_color(color: Union[None, str, callable], state: ILocation, default: str):
    """
    Return a matplotlib color string depending on the type of `color`

    :param color: `string` to pass through, `None` to use default or `callable` to use a function.
    :param state: The location to use if `color` is a `callable`.
    :param default: Default color value if `None` was passed.
    :rtype: str
    """
    if color is None:
        return default
    elif type(color) is str:
        return color
    elif callable(color):
        return color(state)
    else:
        raise TypeError
